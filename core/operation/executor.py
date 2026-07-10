"""
BSR Operation Executor

Operation → 参数校验 → Constraint 复核 → 写 IFC → History 记录

指定层：Runtime
"""

from dataclasses import dataclass, field
from typing import Any, Optional
import os
from datetime import datetime

import ifcopenshell

from core.history.change import Change


_OPERATION_TABLE = {
    "SelectElement":      {"required_params": ["element_id"]},
    "SelectByType":       {"required_params": ["ifc_class"]},
    "SelectByProperty":   {"required_params": ["property", "value"]},
    "ModifyProperty":     {"required_params": ["element_id", "property", "value"]},
    "CreateElement":      {"required_params": ["ifc_class"]},
    "DeleteElement":      {"required_params": ["element_id", "reason"]},
}


@dataclass
class Operation:
    name: str
    params: dict
    protection_level: int = 1
    agent_prompt: str = ""


@dataclass
class OperationResult:
    operation: str
    status: str = ""  # success, rejected, pending_approval
    affected_ids: list = field(default_factory=list)
    snapshot_id: str = ""
    constraint_results: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


class BSRExecutor:
    """操作执行器：校验 → Constraint → 写 IFC → History"""

    def __init__(self, protected: bool = False):
        self._protected = protected
        self._constraint_engine_fn = None
        self._history_store_fn = None

    def register_engine(self, engine_fn):
        self._constraint_engine_fn = engine_fn

    def register_history(self, store_fn):
        self._history_store_fn = store_fn

    def execute(self, op: Operation, ifc_path: str, out_path: str = "",
                transaction_id: str = "") -> OperationResult:
        out = out_path or ifc_path
        result = OperationResult(operation=op.name)

        try:
            # 参数校验
            if op.name not in _OPERATION_TABLE:
                return self._reject(result, f"Unknown operation: {op.name}")
            if not os.path.isfile(ifc_path):
                return self._reject(result, f"IFC file not found: {ifc_path}")

            op_def = _OPERATION_TABLE[op.name]
            for p in op_def.get("required_params", []):
                if p not in op.params:
                    return self._reject(result, f"Missing param: {p}")

            # Constraint 复核（L2+）
            if op.protection_level >= 2 and self._constraint_engine_fn:
                model = ifcopenshell.open(ifc_path)
                engine = self._constraint_engine_fn()
                c_results = engine.check_all(model)
                c_summary = engine.summary(c_results)
                result.constraint_results = [
                    {"rule": r.rule, "passed": r.passed,
                     "element_id": r.element_id, "message": r.message}
                    for r in c_results
                ]
                if not c_summary["passed_all"]:
                    failed_rules = [r for r in c_results if not r.passed]
                    result.status = "rejected"
                    result.errors.append(f"Constraint check failed: {failed_rules[0].rule} on {failed_rules[0].element_id} — {failed_rules[0].message}")
                    return result

            # 人工确认（L3+ & protected）
            if op.protection_level >= 3 and self._protected:
                result.status = "pending_approval"
                return result

            # 写 IFC
            model = ifcopenshell.open(ifc_path)
            affected = self._apply(model, op)
            model.write(out)
            result.affected_ids = affected

            # History 记录
            if self._history_store_fn:
                store = self._history_store_fn()
                store.record_change(Change(
                    element_id=op.params.get("element_id", ""),
                    property_name=op.params.get("property", ""),
                    before=str(op.params.get("old_value", "")),
                    after=str(op.params.get("value", "")),
                    operation=op.name,
                    agent_prompt=op.agent_prompt or "",
                    transaction_id=transaction_id,
                ))
                if op.protection_level >= 4:
                    snap = store.create_snapshot(out)
                    result.snapshot_id = snap.snapshot_id

            result.status = "success"

        except Exception as e:
            result.status = "rejected"
            result.errors.append(str(e))

        return result

    def _reject(self, result, msg):
        result.status = "rejected"
        result.errors.append(msg)
        return result

    @staticmethod
    def _resolve_element(model, element_id: str):
        """按 ID 或 Name 查找元素"""
        try:
            eid = int(element_id.lstrip("#"))
            el = model.by_id(eid)
            if el:
                return el
        except (ValueError, RuntimeError):
            pass
        # 按名称查找
        for el in list(model.by_type("IfcBuildingElementProxy")) + list(model.by_type("IfcWall")):
            if el.Name and el.Name.strip() == element_id.strip():
                return el
        return None

    @staticmethod
    def _apply(model, op: Operation) -> list:
        el_id = op.params.get("element_id", "")
        prop = op.params.get("property", "")
        value = op.params.get("value", None)

        if op.name == "ModifyProperty":
            if not el_id or not prop or value is None:
                return []
            el = BSRExecutor._resolve_element(model, el_id)
            if not el:
                return []
            # Depth 是嵌套属性，藏在 Representation.Items[0]
            if prop in ("Depth", "depth"):
                if el.Representation:
                    for rep in (el.Representation.Representations or []):
                        for it in (rep.Items or []):
                            if hasattr(it, 'Depth'):
                                old = float(it.Depth)
                                op.params["old_value"] = str(old)
                                it.Depth = float(value)
                                return [str(el.id())]
                return []
            old = getattr(el, prop, None)
            op.params["old_value"] = str(old) if old is not None else ""
            setattr(el, prop, type(old)(value) if old is not None else value)
            return [str(el.id())]

        return []

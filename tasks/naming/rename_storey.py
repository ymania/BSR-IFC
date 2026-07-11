"""
BSR Task — rename-storey

工程语言: "把楼层名统一成 1F/2F/3F 格式"

按 Elevation 排序，把 IfcBuildingStorey 的 Name 改成正规定义：
地下一层 → B1, 首层 → 1F, 二层 → 2F, 屋顶 → RF
"""
from dataclasses import dataclass, field
from core.history.change import HistoryStore
from core.operation.executor import BSRExecutor, Operation


_STOREY_NAMES = {
    "B1": (-4.0, -2.0),
    "1F": (-2.0, 2.0),
    "2F": (2.0, 6.0),
    "3F": (6.0, 10.0),
    "4F": (10.0, 14.0),
    "RF": (14.0, 999.0),
}


def _elevation_to_name(elev: float) -> str:
    for name, (lo, hi) in sorted(_STOREY_NAMES.items(), key=lambda x: x[1][0]):
        if lo <= elev < hi:
            return name
    return f"FL{int(elev)}"


@dataclass
class TaskInput:
    ifc_path: str = ""
    mapping: str = ""  # JSON 自定义映射，空=自动
    dry_run: bool = False
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "rename-storey"
    status: str = ""
    operations: int = 0
    modified: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    tx_id: str = ""


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    storeys = sorted(
        [st for st in model.by_type("IfcBuildingStorey")],
        key=lambda s: float(s.Elevation or 0)
    )

    if not storeys:
        report.status = "rejected"
        report.errors.append("No IfcBuildingStorey found")
        return report

    if inp.dry_run:
        report.status = "success"
        report.operations = len(storeys)
        report.modified = [{"element": f"#{s.id()}", "old": s.Name or "-", "new": _elevation_to_name(float(s.Elevation or 0))} for s in storeys]
        return report

    store = HistoryStore(HistoryStore.db_path_for(inp.ifc_path))
    exe = BSRExecutor(protected=inp.protected)
    store.create_snapshot(inp.ifc_path, "before rename-storey")
    tx_id = store.begin_tx(f"rename-storey: {len(storeys)} storeys")

    modified = []
    for s in storeys:
        old_name = s.Name or f"#{s.id()}"
        new_name = _elevation_to_name(float(s.Elevation or 0))
        op = Operation(
            name="ModifyProperty",
            params={"element_id": f"#{s.id()}", "property": "Name", "value": new_name},
            protection_level=1,
            agent_prompt=f"rename storey {old_name} → {new_name}",
        )
        r = exe.execute(op, inp.ifc_path, inp.ifc_path, transaction_id=tx_id)
        if r.status == "success":
            modified.append({"element": f"#{s.id()}", "old": old_name, "new": new_name})
        else:
            report.errors.append(f"#{s.id()} {old_name}: {r.errors}")

    if report.errors:
        store.abort_tx(tx_id)
        report.status = "rejected"
        report.tx_id = tx_id
        return report

    store.commit_tx(tx_id)
    report.status = "success"
    report.operations = len(modified)
    report.modified = modified
    report.tx_id = tx_id
    return report

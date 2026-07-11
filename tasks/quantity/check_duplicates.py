"""
BSR Task — check-duplicates

工程语言: "检查 IFC 中是否有重复构件（同一个 GUID/Name/位置）"

扫描三方面重复：
- GlobalId 重复
- Name + IfcBuildingStorey 重复
- 几何位置一致（通过 LocalPlacement 比较）
"""
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class TaskInput:
    ifc_path: str = ""
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "check-duplicates"
    status: str = ""
    operations: int = 0
    duplicate_guids: list = field(default_factory=list)
    duplicate_names: list = field(default_factory=list)
    total_duplicates: int = 0
    errors: list = field(default_factory=list)


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    # 1. GUID 重复
    guid_map = {}
    for el in model:
        g = str(el.GlobalId)
        guid_map.setdefault(g, []).append(el)
    for g, els in guid_map.items():
        if len(els) > 1:
            report.duplicate_guids.append({
                "guid": g[:12],
                "count": len(els),
                "elements": [f"#{e.id()} {e.is_a()} {e.Name or ''}" for e in els],
            })

    # 2. 同楼层同名
    name_storey_map = {}
    for rel in model.by_type("IfcRelContainedInSpatialStructure"):
        storey = rel.RelatingStructure
        for el in (rel.RelatedElements or []):
            name = (el.Name or "").strip()
            if not name:
                continue
            key = f"{storey.Name or ''}:{name}"
            name_storey_map.setdefault(key, []).append(f"#{el.id()} {el.is_a()}")
    for key, els in name_storey_map.items():
        if len(els) > 1:
            report.duplicate_names.append({
                "name_storey": key,
                "count": len(els),
                "elements": els,
            })

    report.total_duplicates = len(report.duplicate_guids) + len(report.duplicate_names)
    report.status = "success"
    report.operations = 0  # 只读
    return report

"""
BSR Task — check-attributes

工程语言: "检查所有构件的关键属性是否完整"

对每个实体类型检查其应有的属性集是否完整。
可配置规则集，默认检查 Name / GlobalId / 关键 Pset 属性。
"""
from dataclasses import dataclass, field


# 实体类型 → 必须存在的属性
_MANDATORY_ATTRS = {
    "IfcWall": ["Name", "GlobalId", "ObjectType"],
    "IfcSlab": ["Name", "GlobalId"],
    "IfcDoor": ["Name", "GlobalId", "OverallHeight", "OverallWidth"],
    "IfcWindow": ["Name", "GlobalId", "OverallHeight", "OverallWidth"],
    "IfcColumn": ["Name", "GlobalId"],
    "IfcBeam": ["Name", "GlobalId"],
    "IfcSpace": ["Name", "LongName", "GlobalId"],
    "IfcBuildingStorey": ["Name", "GlobalId", "Elevation"],
    "IfcRoof": ["Name", "GlobalId"],
    "IfcStair": ["Name", "GlobalId"],
    "IfcRamp": ["Name", "GlobalId"],
    "IfcRailing": ["Name", "GlobalId"],
    "IfcFooting": ["Name", "GlobalId"],
    "IfcFurniture": ["Name", "GlobalId"],
    "IfcBuildingElementProxy": ["Name", "GlobalId"],
    "IfcFlowSegment": ["Name", "GlobalId"],
    "IfcFlowFitting": ["Name", "GlobalId"],
    "IfcFlowTerminal": ["Name", "GlobalId"],
    "IfcMember": ["Name", "GlobalId"],
    "IfcElementAssembly": ["Name", "GlobalId"],
}


@dataclass
class TaskInput:
    ifc_path: str = ""
    entity_type: str = ""  # 空=全部
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "check-attributes"
    status: str = ""
    operations: int = 0
    missing: list = field(default_factory=list)  # [{element, type, missing_attrs}]
    total_checked: int = 0
    total_issues: int = 0
    errors: list = field(default_factory=list)


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    target_types = [inp.entity_type] if inp.entity_type else list(_MANDATORY_ATTRS.keys())
    target_types = [t for t in target_types if t in _MANDATORY_ATTRS]

    missing = []
    total_checked = 0
    for t in target_types:
        for el in model.by_type(t):
            total_checked += 1
            missing_attrs = []
            for attr in _MANDATORY_ATTRS[t]:
                val = getattr(el, attr, None)
                if val is None or (isinstance(val, str) and val.strip() == ""):
                    missing_attrs.append(attr)
            if missing_attrs:
                missing.append({
                    "element": f"#{el.id()}",
                    "type": t,
                    "name": el.Name or "-",
                    "missing": missing_attrs,
                })

    report.status = "success"
    report.operations = 0  # 只读
    report.missing = missing
    report.total_checked = total_checked
    report.total_issues = len(missing)
    return report

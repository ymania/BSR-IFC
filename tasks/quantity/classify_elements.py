"""
BSR Task — classify-elements

工程语言: "检查构件是否按 IfcBuildingElementProxy 归类到了正确类型"

扫描所有 IfcBuildingElementProxy，看 Name 关键词能匹配到更具体的 IFC 类型
（如 Name="column" → IfcColumn），输出建议重分类的列表。
"""
from dataclasses import dataclass, field


# Name 关键词 → 建议的 IFC 类型
_TYPE_HINTS = {
    "column": "IfcColumn", "pillar": "IfcColumn",
    "beam": "IfcBeam", "girder": "IfcBeam",
    "wall": "IfcWall",
    "slab": "IfcSlab", "floor": "IfcSlab",
    "door": "IfcDoor",
    "window": "IfcWindow",
    "stair": "IfcStair", "stairs": "IfcStair",
    "railing": "IfcRailing", "rail": "IfcRailing",
    "roof": "IfcRoof",
    "footing": "IfcFooting", "foundation": "IfcFooting",
    "pipe": "IfcFlowSegment", "duct": "IfcFlowSegment",
    "furniture": "IfcFurniture", "table": "IfcFurniture", "chair": "IfcFurniture",
    "beam": "IfcBeam",
    "member": "IfcMember",
    "chimney": "IfcChimney",
    "ramp": "IfcRamp",
}


@dataclass
class TaskInput:
    ifc_path: str = ""
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "classify-elements"
    status: str = ""
    operations: int = 0
    misclassified: list = field(default_factory=list)  # [{element, name, suggested_type}]
    correctly_classified: int = 0
    errors: list = field(default_factory=list)


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    misclassified = []
    correct = 0
    for el in model.by_type("IfcBuildingElementProxy"):
        name = (el.Name or "").lower()
        if not name:
            continue
        for keyword, suggested_type in _TYPE_HINTS.items():
            if keyword in name:
                misclassified.append({
                    "element": f"#{el.id()}",
                    "name": el.Name,
                    "current_type": "IfcBuildingElementProxy",
                    "suggested_type": suggested_type,
                    "reason": f"Name contains '{keyword}'",
                })
                break
        else:
            correct += 1

    # 也检查 IfcWall/IfcSlab 等是否有 Name 暗示不同类型（跨类误归）
    cross_checks = [
        ("IfcWall", ["slab", "floor", "door"]),
        ("IfcSlab", ["wall", "column", "beam"]),
        ("IfcBeam", ["wall", "slab"]),
        ("IfcColumn", ["beam", "wall"]),
    ]
    for ifc_class, forbidden_keywords in cross_checks:
        for el in model.by_type(ifc_class):
            name = (el.Name or "").lower()
            for kw in forbidden_keywords:
                if kw in name:
                    misclassified.append({
                        "element": f"#{el.id()}",
                        "name": el.Name,
                        "current_type": ifc_class,
                        "suggested_type": _TYPE_HINTS.get(kw, "?"),
                        "reason": f"Name '{el.Name}' contains '{kw}', may be misclassified",
                    })
                    break

    report.status = "success"
    report.operations = 0  # 只读
    report.misclassified = misclassified
    report.correctly_classified = correct
    return report

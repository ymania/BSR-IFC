"""
BSR Task — element-stats

工程语言: "统计门窗墙柱种类和数量"

按 IFC 实体类型统计构件数量，导出表格。
"""
from dataclasses import dataclass, field
from collections import Counter


# 工程上关心的构件类型
_ELEMENT_TYPES = [
    ("墙", "IfcWall"),
    ("板", "IfcSlab"),
    ("柱", "IfcColumn"),
    ("梁", "IfcBeam"),
    ("门", "IfcDoor"),
    ("窗", "IfcWindow"),
    ("楼梯", "IfcStair"),
    ("坡道", "IfcRamp"),
    ("栏杆", "IfcRailing"),
    ("屋顶", "IfcRoof"),
    ("基础", "IfcFooting"),
    ("家具", "IfcFurniture"),
    ("代理", "IfcBuildingElementProxy"),
    ("空间", "IfcSpace"),
    ("楼层", "IfcBuildingStorey"),
    ("MEP终端", "IfcFlowTerminal"),
    ("MEP段", "IfcFlowSegment"),
    ("MEP配件", "IfcFlowFitting"),
    ("构件", "IfcMember"),
    ("组装", "IfcElementAssembly"),
]


@dataclass
class TaskInput:
    ifc_path: str = ""
    format: str = "table"  # table / json / csv
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "element-stats"
    status: str = ""
    operations: int = 0
    stats: list = field(default_factory=list)  # [{type, ifc_class, count}, ...]
    total_elements: int = 0
    filled: list = field(default_factory=list)
    errors: list = field(default_factory=list)


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    counts = Counter()
    for t in model:
        counts[t.is_a()] += 1

    total = 0
    stats = []
    for cn_name, ifc_class in _ELEMENT_TYPES:
        c = counts.get(ifc_class, 0)
        if c > 0:
            stats.append({"type": cn_name, "ifc_class": ifc_class, "count": c})
            total += c

    # 未列出的其他类型
    listed = set(ic for _, ic in _ELEMENT_TYPES)
    other = sum(c for t, c in counts.items() if t not in listed)

    report.status = "success"
    report.operations = 0  # 只读
    report.stats = stats
    report.total_elements = len(list(model))
    report.filled = []  # 用于 CLI 显示
    return report

"""
BSR Task — room-area-summary

工程语言: "汇总所有房间面积"

从 IfcSpace 的 Pset_SpaceCommon 提取 GrossPlannedArea / NetPlannedArea，
按楼层组织输出。
"""
from dataclasses import dataclass, field


@dataclass
class TaskInput:
    ifc_path: str = ""
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "room-area-summary"
    status: str = ""
    operations: int = 0
    rooms: list = field(default_factory=list)  # [{storey, name, gross, net}, ...]
    total_gross: float = 0.0
    total_net: float = 0.0
    errors: list = field(default_factory=list)


def _get_space_area(space) -> tuple:
    """从空间关联的 PropertySet 中提取 GrossPlannedArea 和 NetPlannedArea
    使用 IsDefinedBy (IfcRelDefinesByProperties 的 inverse 属性)。"""
    gross = None
    net = None
    for rel in (space.IsDefinedBy or []):
        if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition:
            ps = rel.RelatingPropertyDefinition
            if ps.is_a("IfcPropertySet") and ps.Name == "Pset_SpaceCommon":
                for p in (ps.HasProperties or []):
                    if p.Name == "GrossPlannedArea":
                        gross = float(p.NominalValue.wrappedValue if hasattr(p.NominalValue, 'wrappedValue') else p.NominalValue)
                    elif p.Name == "NetPlannedArea":
                        net = float(p.NominalValue.wrappedValue if hasattr(p.NominalValue, 'wrappedValue') else p.NominalValue)
    return gross, net


def run(inp: TaskInput) -> TaskReport:
    import ifcopenshell
    report = TaskReport()
    model = ifcopenshell.open(inp.ifc_path)

    # 楼层→Name 映射
    storey_names = {}
    for st in model.by_type("IfcBuildingStorey"):
        storey_names[st.id()] = st.Name or f"#{st.id()}"

    # 元素→楼层映射
    el_to_storey = {}
    for rel in model.by_type("IfcRelContainedInSpatialStructure"):
        storey_id = rel.RelatingStructure.id()
        for el in (rel.RelatedElements or []):
            el_to_storey[el.id()] = storey_id

    rooms = []
    total_gross = 0.0
    total_net = 0.0
    for space in model.by_type("IfcSpace"):
        storey_id = el_to_storey.get(space.id())
        storey_name = storey_names.get(storey_id, "-") if storey_id else "-"
        gross, net = _get_space_area(space)
        if gross is None and net is None:
            continue
        gross = gross or 0.0
        net = net or 0.0
        rooms.append({
            "storey": storey_name,
            "name": space.Name or f"#{space.id()}",
            "gross": round(gross, 2),
            "net": round(net, 2),
        })
        total_gross += gross
        total_net += net

    report.status = "success"
    report.operations = 0  # 只读
    report.rooms = rooms
    report.total_gross = round(total_gross, 2)
    report.total_net = round(total_net, 2)
    return report

# BSR 拓扑约束
# 未来扩展：墙不能悬空、窗必须在墙上等

from dataclasses import dataclass
from typing import List
from core.constraint.engine import ConstraintResult


@dataclass
class ElementHasParentRule:
    """每个 IfcBuildingElement 必须在 IfcBuildingStorey 下"""
    def check(self, model) -> List[ConstraintResult]:
        results = []
        storey_elements = set()
        for rel in model.by_type("IfcRelContainedInSpatialStructure"):
            for el in rel.RelatedElements or []:
                storey_elements.add(el.id())
        
        for el in list(model.by_type("IfcBuildingElementProxy")) + list(model.by_type("IfcWall")):
            in_storey = el.id() in storey_elements
            name = el.Name or f"#{el.id()}"
            results.append(ConstraintResult(
                rule="ElementHasParentRule",
                passed=in_storey,
                element_id=f"#{el.id()}",
                message=f"{name}: {'in storey' if in_storey else 'NOT in any storey'}"
            ))
        return results

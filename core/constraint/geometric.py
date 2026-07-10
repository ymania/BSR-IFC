# BSR 几何约束

from dataclasses import dataclass, field
from typing import List
from core.constraint.engine import ConstraintResult


@dataclass
class DepthRangeRule:
    """ExtrudedAreaSolid 的 Depth 必须在合理范围。按构件类型分化阈值。"""
    min_d: float = 0.1
    max_d: float = 20.0
    # 按构件类型分化（名称中包含关键词自动匹配）
    type_thresholds: dict = field(default_factory=lambda: {
        "grass": (0.01, 1.0),
        "plant": (0.01, 5.0),
        "tree": (0.1, 10.0),
        "sidewalk": (0.05, 1.0),
        "sculpture": (0.1, 5.0),
        "building": (0.1, 20.0),
        "wall": (0.1, 20.0),
    })

    def _get_threshold(self, name: str):
        name_lower = name.lower()
        for keyword, (lo, hi) in self.type_thresholds.items():
            if keyword in name_lower:
                return lo, hi
        return self.min_d, self.max_d

    def check(self, model) -> List[ConstraintResult]:
        results = []
        for el in list(model.by_type("IfcBuildingElementProxy")) + list(model.by_type("IfcWall")):
            if el.Representation:
                for rep in el.Representation.Representations or []:
                    for item in rep.Items:
                        if item.is_a("IfcExtrudedAreaSolid"):
                            d = float(item.Depth)
                            name = el.Name or f"#{el.id()}"
                            lo, hi = self._get_threshold(name)
                            if d < lo:
                                results.append(ConstraintResult(
                                    rule="DepthRangeRule",
                                    passed=False,
                                    element_id=f"#{el.id()}",
                                    message=f"{name} Depth={d:.2f}m < min({lo:.2f}m) for type"
                                ))
                            elif d > hi:
                                results.append(ConstraintResult(
                                    rule="DepthRangeRule",
                                    passed=False,
                                    element_id=f"#{el.id()}",
                                    message=f"{name} Depth={d:.2f}m > max({hi:.2f}m) for type"
                                ))
                            else:
                                results.append(ConstraintResult(
                                    rule="DepthRangeRule",
                                    passed=True,
                                    element_id=f"#{el.id()}",
                                    message=f"{name} Depth={d:.2f}m ok"
                                ))
        return results


@dataclass
class GeometryExistsRule:
    """每个构件必须有几何表示"""
    def check(self, model) -> List[ConstraintResult]:
        results = []
        for el in list(model.by_type("IfcBuildingElementProxy")) + list(model.by_type("IfcWall")):
            name = el.Name or f"#{el.id()}"
            has_shape = el.Representation is not None
            results.append(ConstraintResult(
                rule="GeometryExistsRule",
                passed=has_shape,
                element_id=f"#{el.id()}",
                message=f"{name}: {'has geometry' if has_shape else 'NO geometry'}"
            ))
        return results

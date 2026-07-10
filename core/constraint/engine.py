# BSR Constraint — 规则引擎入口

"""
BSR 约束引擎：Agent 修改 IFC 后的合法性检查。
像 Aider 的"代码必须能编译"——这里"IFC 必须合规"。
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ConstraintResult:
    rule: str
    passed: bool
    element_id: str = ""
    message: str = ""


class ConstraintEngine:
    """
    约束引擎：注册规则 → 对 IFC 逐一检查 → 汇总结果。
    所有新增规则只需实现 check(model) → [ConstraintResult] 接口。
    """

    def __init__(self):
        self._rules: List[Any] = []

    def register(self, rule):
        self._rules.append(rule)

    def check_all(self, model) -> List[ConstraintResult]:
        results = []
        for rule in self._rules:
            try:
                results.extend(rule.check(model))
            except Exception as e:
                results.append(ConstraintResult(
                    rule=rule.__class__.__name__,
                    passed=False,
                    message=f"Rule error: {e}"
                ))
        return results

    def summary(self, results: List[ConstraintResult]) -> Dict:
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed)
        return {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "passed_all": failed == 0,
        }

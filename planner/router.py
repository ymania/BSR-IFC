"""
BSR Planner — 任务路由

bsr task <name> [args...]

不需要 LLM。纯路由表：任务名 → 对应 run 函数 → 执行 → 返回报告。
"""

from typing import Optional
from dataclasses import dataclass, field


_task_registry = {}


def register(name: str, run_fn):
    _task_registry[name] = run_fn


def list_tasks() -> list:
    return sorted(_task_registry.keys())


def run_task(name: str, input_data) -> Optional[dict]:
    fn = _task_registry.get(name)
    if not fn:
        return None
    report = fn(input_data)
    return {
        "task": name,
        "status": report.status,
        "operations": getattr(report, 'operations', 0),
        "modified": getattr(report, 'modified', []),
        "filled": getattr(report, 'filled', []),
        "stats": getattr(report, 'stats', []),
        "issues": getattr(report, 'missing', getattr(report, 'issues', [])),
        "duplicate_guids": getattr(report, 'duplicate_guids', []),
        "duplicate_names": getattr(report, 'duplicate_names', []),
        "total_duplicates": getattr(report, 'total_duplicates', 0),
        "total_issues": getattr(report, 'total_issues', 0),
        "misclassified": getattr(report, 'misclassified', []),
        "rooms": getattr(report, 'rooms', []),
        "total_elements": getattr(report, 'total_elements', 0),
        "total_gross": getattr(report, 'total_gross', 0.0),
        "total_net": getattr(report, 'total_net', 0.0),
        "report_text": getattr(report, 'report_text', ""),
        "errors": getattr(report, 'errors', []),
    }

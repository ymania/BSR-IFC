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
        "errors": getattr(report, 'errors', []),
    }

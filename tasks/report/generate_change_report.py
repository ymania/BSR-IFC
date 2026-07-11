"""
BSR Task — generate-change-report

工程语言: "生成从初始状态到当前的所有变更报告"

读取 HistoryStore 中所有 change 记录和 snapshot 信息，
输出结构化变更报告（可 JSON/table/markdown）。
"""
from dataclasses import dataclass, field
import json


@dataclass
class TaskInput:
    ifc_path: str = ""
    format: str = "table"  # table / json / markdown
    since_snapshot: str = ""  # 空=从头开始
    protected: bool = False


@dataclass
class TaskReport:
    task: str = "generate-change-report"
    status: str = ""
    operations: int = 0
    changes: list = field(default_factory=list)
    snapshots: list = field(default_factory=list)
    total_changes: int = 0
    report_text: str = ""
    errors: list = field(default_factory=list)


def run(inp: TaskInput) -> TaskReport:
    from core.history.change import HistoryStore
    report = TaskReport()
    store = HistoryStore(HistoryStore.db_path_for(inp.ifc_path))

    # 获取所有 changes
    rows = store.get_history(1000)
    changes = []
    for r in rows:
        changes.append({
            "id": r[0],
            "element": r[1],
            "property": r[2],
            "before": (r[3] or "")[:20],
            "after": (r[4] or "")[:20],
            "operation": r[5],
            "timestamp": r[6][:19] if r[6] else "",
            "tx_id": r[7] or "",
        })

    # 获取 snapshots
    snap_rows = store.conn.execute(
        "SELECT snapshot_id, ifc_hash, timestamp, description FROM snapshots ORDER BY timestamp"
    ).fetchall()
    snapshots = [{"id": s[0], "hash": s[1][:12], "time": s[2][:19], "desc": s[3]} for s in snap_rows]

    # 生成文本报告
    lines = []
    lines.append("=" * 50)
    lines.append("BSR 变更报告")
    lines.append("=" * 50)
    lines.append(f"总修改次数: {len(changes)}")
    lines.append(f"总快照数: {len(snapshots)}")
    lines.append("")

    if snapshots:
        lines.append("--- 快照 ---")
        for s in snapshots:
            lines.append(f"  {s['id']} | {s['time']} | {s['desc']}")
        lines.append("")

    if changes:
        lines.append("--- 变更明细 ---")
        for c in changes:
            lines.append(f"  #{c['id']} [{c['operation'][:12]}] {c['element']}.{c['property']}: {c['before']} → {c['after']}  @{c['timestamp']}")

    lines.append("")
    lines.append("=" * 50)

    report.status = "success"
    report.operations = 0  # 只读
    report.changes = changes
    report.snapshots = snapshots
    report.total_changes = len(changes)
    report.report_text = "\n".join(lines)

    if inp.format == "json":
        report.report_text = json.dumps({"changes": changes, "snapshots": snapshots}, indent=2, ensure_ascii=False)

    return report

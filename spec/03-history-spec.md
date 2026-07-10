# BSR History Spec v0.1

> **每次操作的修改记录。**
> 像 Git 管理代码版本一样管理 IFC 数据版本。

---

## 核心概念

| BSR | Git 类比 | 说明 |
|-----|---------|------|
| Change | commit | 一次操作前后对比 |
| Snapshot | tag | 全量 IFC 快照（关键节点） |
| Rollback | revert | 恢复到指定 Snapshot |
| Diff | git diff | 两个 IFC 的增量对比 |

**设计原则**：尽量增量，少全量。
- 日常操作只记录 Change（before/after 属性差）
- 关键节点（提交给客户前、批量修改前）才做 Full Snapshot
- Rollback 时按 Change 链反向逐条恢复，或直接跳到最近 Snapshot

---

## Change

每次 Agent 操作后记录一条 Change。

| 字段 | 类型 | 说明 |
|------|------|------|
| element_id | string | 被修改的元素 ID |
| property_name | string | 被修改的属性名 |
| before_value | string | 修改前的值（序列化） |
| after_value | string | 修改后的值 |
| operation | string | 发起的 Operation 名 |
| agent_prompt | string | Agent 的自然语言指令 |
| timestamp | string | ISO 时间 |

Change 存储在本地 SQLite，按时间倒序可查。

---

## Snapshot

全量 IFC 快照，不常做。

| 字段 | 类型 | 说明 |
|------|------|------|
| snapshot_id | string | 唯一 ID，格式 `bsr-snap-{YYYYMMDD}-{HHMMSS}` |
| ifc_path | string | 对应 IFC 文件路径 |
| ifc_hash | string | 文件 SHA256 前 12 位 |
| timestamp | string | ISO 时间 |
| parent_id | string | 基于哪个 Snapshot 创建（留空表示首次） |

---

## Rollback

两种回滚模式：

**增量回滚**：把 Change 链从最新到目标逐条反向执行（`after → before`）。
适用：小幅误改（最近几次操作）。

**快照恢复**：直接用目标 Snapshot 的 IFC 文件覆盖当前。
适用：大幅误操作（批量删改等）。

---

## Diff

比较两个 IFC 文件/两个历史版本的结构化差异：

```json
{
  "added": ["#101", "#102"],
  "modified": [
    {"element": "#37", "property": "Depth", "before": "4.0000", "after": "4.5000"}
  ],
  "deleted": ["#57"]
}
```

Diff 基于元素 ID 匹配，不是文本行 diff——因为 IFC 是结构化数据。

---

## 存储实现

本地 SQLite，两张表：

```sql
CREATE TABLE changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    element_id TEXT,
    property_name TEXT,
    before_value TEXT,
    after_value TEXT,
    operation TEXT,
    agent_prompt TEXT,
    timestamp TEXT
);

CREATE TABLE snapshots (
    snapshot_id TEXT PRIMARY KEY,
    ifc_path TEXT,
    ifc_hash TEXT,
    timestamp TEXT,
    parent_id TEXT
);
```

变更历史留存策略：按周轮转或按 Snapshot 数上限清理。

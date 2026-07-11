# 协议

BSR 定义四份协议层：

## P1 — 操作协议 (Operation Protocol)

用户与 BSR 之间交互的规范。

```
模式 A: 自然语言 → `bsr set model.ifc "把 #37 的 Depth 改成 4.0"`
模式 B: 参数命令 → `bsr set model.ifc element=#37 depth=4.0`
模式 C: 工程任务 → `bsr task rename-room model.ifc --prefix Room-`
```

## P2 — 约束协议 (Constraint Protocol)

约束引擎验证规则的标准格式。

```json
{
  "rule_id": "FIRE-001",
  "name": "疏散距离 ≤ 30m",
  "target": "IfcSpace",
  "check": "distance_to_nearest_exit <= 30",
  "severity": "error"
}
```

## P3 — 历史协议 (History Protocol)

版本管理的数据结构。

```json
{
  "transaction": {
    "id": "txn-a3f2e1",
    "operations": ["modify #37 Depth 3.0→4.0"],
    "timestamp": "2026-07-10T15:30:00Z",
    "parent": "txn-a3f2e0"
  }
}
```

## P4 — 任务协议 (Task Protocol)

Task Library 的接口规范。

```python
class Task:
    name: str              # rename-room
    description: str       # 重命名房间
    params: list[Param]    # prefix, floor
    operations: list[str]  # 分解为原子操作
    constraints: list[str] # 相关约束规则
```

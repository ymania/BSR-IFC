# BSR Operation Spec v0.1

> **Agent 允许对 IFC 做什么。**
> 类似 CPU 的 ISA。任何 Agent 只能通过这里定义的操作与 IFC 数据交互。

---

## 操作原语

### Select（读取）

| Operation | 输入 | 输出 | 防护等级 |
|-----------|------|------|---------|
| SelectElement | Element ID | Element | L1 |
| SelectByType | IFC Class (list) | [Element] | L1 |
| SelectByProperty | Property, Value | [Element] | L1 |
| SelectBySpatial | IfcBuildingStorey | [Element] | L1 |
| QueryRelationship | Element ID | [Related Elements] | L1 |

### Create（创建）

| Operation | 输入 | 输出 | 防护等级 |
|-----------|------|------|---------|
| CreateElement | IFC Class, Geometry, Properties | Element ID | L2 |
| CreateRelationship | Type, Source, Target | Relationship ID | L1 |

Create 操作的几何参数必须通过 Constraint 校验才写入。

### Modify（修改）

| Operation | 输入 | 输出 | 防护等级 |
|-----------|------|------|---------|
| ModifyProperty | Element ID, Property, Value | Modified IDs | L2 |
| ModifyGeometry | Element ID, Geometry Params | Modified IDs | L2 |
| MoveElement | Element ID, Position | Modified IDs | L2 |
| RotateElement | Element ID, Rotation | Modified IDs | L2 |
| ReplaceElement | Element ID, New Params | Modified IDs | L3 |

### Delete（删除）

| Operation | 输入 | 输出 | 防护等级 |
|-----------|------|------|---------|
| DeleteElement | Element ID, Reason | Rollback Token | L4 |
| DeleteRelationship | Relationship ID | Rollback Token | L3 |

---

## 防护等级

| 等级 | 规则 |
|------|------|
| L1 | 自动执行，写入 History |
| L2 | Constraint Engine 复核通过才提交 |
| L3 | Constraint Engine 复核 + 人工确认（PROTECTED=true 时） |
| L4 | 必须显式传入 Delete Reason + Constraint Engine + 自动创建 Full Snapshot + PROTECTED 时人工确认 |

L3/L4 修改后自动级联检查相关元素（移动墙后检查门窗位置）。
Delete L4 级联检查：删除墙 → 检查该墙上的门窗是否需要一并处理。

---

## 禁止操作

- 不能直接修改 GUID（IfcGloballyUniqueId）
- 不能修改 OwnerHistory
- 不能删除 IfcProject / IfcSite / IfcBuilding 根节点
- 不能直接修改 IfcRelAggregates 关系链头尾

---

## 操作执行流程

```
User / Agent 发起 Operation
          ↓
    参数校验（类型 + 范围）
          ↓
    [L2+] → Constraint Engine 复核
          ↓
    [L3+] → 人工确认（PROTECTED）
          ↓
    写入 IFC 数据
          ↓
    Schema 验证（ifcopenshell 级别）
          ↓
    History 记录（before/after）
          ↓
    返回 Operation Result
```

---

## Operation Result 格式

```json
{
  "operation": "ModifyProperty",
  "status": "success" | "rejected" | "pending_approval",
  "affected_ids": ["#37"],
  "snapshot_id": "bst-snap-20260710-001",
  "constraint_results": [
    {"rule": "DepthRangeRule", "passed": true}
  ],
  "warnings": [],
  "errors": []
}
```

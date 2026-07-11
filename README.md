# BSR-IFC — Building State Runtime for IFC

> 像 Aider 操作代码一样操作 IFC 数据。

---

## 一句话

不卖 Agent，不卖 UI，卖一个 IFC 数据的操作规范 + 约束引擎 + 版本管理基础设施。Agent 只是调用者。

**目标**：一个真实工程人员，一句话完成过去半天到一天的工作。

## 示例

下面是建筑生命周期中实际的 IFC 操作场景。每条对话对应一个真实工程问题。

### 🌰 示例 1 — 房间重命名

> **工程人员**：把#37 的 Depth 改成 4.0
>
> **BSR**：已修改 IfcWallStandardCase(#37) Depth 3.0 → 4.0。在优化计算后，所有相关构件（窗台高度、幕墙网格）已自动更新。

```json
{
  "operation": "modify",
  "target": "#37",
  "attribute": "Depth",
  "old_value": 3.0,
  "new_value": 4.0,
  "impact": ["window-sill-height: 14", "curtain-wall-grid: B/2"]
}
```

### 🌰 示例 2 — 消防合规检查

> **工程人员**：检查疏散距离，不符合的标记出来
>
> **BSR**：共 3 处不合格。Room-201 最近出口距离 42m（限 30m），已标记高亮。

| Room | 最近出口 | 实际距离 | 规范上限 | 状态 |
|------|---------|---------|---------|------|
| Room-201 | EXIT-04 | 42m | 30m | ❌ |
| Corridor-A | EXIT-01 | 36m | 30m | ❌ |
| Room-105 | EXIT-03 | 28m | 30m | ✅ |

3 处不合格，建议路径：`bsr task fix-evacuation --file model.ifc`

### 🌰 示例 3 — 构件查询

> **工程人员**：这个项目里有哪些类型的柱子？
>
> **BSR**：共 24 根 IfcColumn，分 3 种类型：

| Type | Count | Max Height | Material |
|------|-------|-----------|----------|
| Rectangular 600×600 | 14 | 4.2m | C30 |
| Circular D500 | 6 | 3.6m | C35 |
| Rectangular 800×400 | 4 | 5.0m | C40 |

### 🌰 示例 4 — 版本回滚

> **工程人员**：刚才改成地下室净高 3.0m，但暖通说送风井道不够。恢复上一版。
>
> **BSR**：已回滚到 Commit a3f2e1。回滚操作撤销了 3 次修改。对比：basement-height 2.8m ← 3.0m。

```
✔ bsr log building.ifc
  ├─ HEAD 修改地下室净高 3.0m
  ├─ a3f2e1 修改空调机房位置
  └─ a3f2e0 初始版本 净高 2.8m
```

---

## 架构

见 `docs/architecture.md`。

## 协议

见 `docs/protocol.md`。

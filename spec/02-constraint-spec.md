# BSR Constraint Spec v0.1

> **什么才算"合法修改"。**
> 像 Aider 的"代码必须能编译"——这里"IFC 必须合规"。

---

## 约束层级

```
Layer 1: Schema 合规     ← ifcopenshell 级别验证
Layer 2: 几何合理性       ← 数值范围、空间关系
Layer 3: 拓扑完整性       ← 构件依存关系
Layer 4: 语义一致性       ← 类型-属性匹配
Layer 5: 工程规则         ← 用户可配置的领域约束
```

---

## Schema 合规（Layer 1）

验证修改后的 IFC 文件是否符合 ISO 16739 标准。

- 实体类型必须存在于 IFC4 schema
- 必填属性不可为空
- 引用完整性（IfcRelAggregates 指向的实体必须存在）
- 几何表示的参数类型正确

**实现**：ifcopenshell.validate()。
**拦截**：Schema 不合规 → 拒绝操作，返回具体错误。

---

## 几何合理性（Layer 2）

| 规则 | 参数 | 说明 |
|------|------|------|
| DepthRange | min=0.1, max=20.0 | ExtrudedAreaSolid 的 Depth 范围 |
| BBoxNonEmpty | — | 包围盒各轴长度 > 0 |
| GeometryExists | — | 每个 BuildingElement 必须有几何表示 |
| DimensionScale | — | 构件尺寸不能超过建筑总尺寸 |

几何规则可按构件类型分化：
- wall/building → Depth 0.1~20.0
- vegetation/grass → Depth 0.01~5.0
- door/window → Depth 0.01~0.5

---

## 拓扑完整性（Layer 3）

| 规则 | 说明 |
|------|------|
| ElementInStorey | 每个 BuildingElement 必须在 IfcBuildingStorey 下 |
| ParentExists | IfcOpeningElement 必须有关联的父元素（IfcRelVoidsElement） |
| RelAggregatesComplete | IfcProject→IfcSite→IfcBuilding→IfcBuildingStorey 关系链完整 |
| NoDanglingElements | 删除元素时，其子关系必须一并处理 |

---

## 语义一致性（Layer 4）

| 规则 | 说明 |
|------|------|
| TypePropertyMatch | IfcWall 必须有 IfcWall 属性集，不能有 IfcSlab 属性 |
| MaterialExists | IfcWall/IfcSlab 应有材质属性 |
| GUIDUnique | 所有 GUID 在文件范围内唯一 |
| NameNotEmpty | 关键构件（Wall, Slab, Window）名称不可为空 |

---

## 工程规则（Layer 5）

用户可配置的规则集，通过 JSON 文件定义：

```json
{
  "wall_min_height": 2.0,
  "wall_max_height": 6.0,
  "door_min_width": 0.6,
  "door_max_width": 2.0,
  "window_must_be_on_wall": true,
  "floor_cannot_float": true,
  "beam_must_have_column": true,
  "stair_max_slope_deg": 45
}
```

Layer 5 规则不内置在 BSR 中，由用户按项目配置。

---

## 约束执行

```
Operation 到达
     ↓
 Layer 1 Schema    → fail → REJECTED
     ↓ pass
 Layer 2 Geometric  → fail → REJECTED + 具体规则名+值
     ↓ pass
 Layer 3 Topology   → fail → REJECTED + 缺少的关系
     ↓ pass
 Layer 4 Semantic   → fail → REJECTED + 错误的属性
     ↓ pass
 Layer 5 Rules      → fail → PENDING 人工复核
     ↓ pass
 Operation 提交 → History 记录
```

## ConstraintResult 格式

```json
{
  "rule": "DepthRangeRule",
  "passed": true,
  "element_id": "#37",
  "message": "building_0 Depth=4.35m ok",
  "layer": 2
}
```

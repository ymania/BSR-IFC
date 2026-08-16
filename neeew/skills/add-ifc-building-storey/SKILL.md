---
name: bsr-add-ifc-building-storey
description: |-
  BSR engineering task: 如果不存在，创建 IfcBuildingStorey 层级. Use when the user needs to 如果不存在，创建 IfcBuildingStorey 层级 in an IFC/BIM file. Applicable when the model has IFC without storey hierarchy.
  TRIGGER — use whenever: the user mentions 如果不存在，创建 IfcBuildingStorey 层级; the IFC contains IFC without storey hierarchy; or the user asks to fix/check/rename/report related to IfcBuildingStorey, IfcRelAggregates.
license: MIT
---

# BSR Task — add-ifc-building-storey

> Task Library: `Task040` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 如果不存在，创建 IfcBuildingStorey 层级
- **Input**: IFC without storey hierarchy
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task add-ifc-building-storey <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcBuildingStorey, IfcRelAggregates) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with IfcBuildingStorey and IfcRelAggregates
- **Constraint**: Project → Site → Building → Storey structure
- **Affected Classes**: IfcBuildingStorey, IfcRelAggregates

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenHouse tutorial; BIM spatial hierarchy requirement
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
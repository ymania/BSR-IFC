---
name: bsr-create-ifc-project-structure
description: |-
  BSR engineering task: 创建完整的 IFC 项目骨架（Project→Site→Building→Storey）. Use when the user needs to 创建完整的 IFC 项目骨架（Project→Site→Building→Storey） in an IFC/BIM file. Applicable when the model has Empty or minimal IFC.
  TRIGGER — use whenever: the user mentions 创建完整的 IFC 项目骨架（Project→Site→Building→Storey）; the IFC contains Empty or minimal IFC; or the user asks to fix/check/rename/report related to IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey.
license: MIT
---

# BSR Task — create-ifc-project-structure

> Task Library: `Task042` · Difficulty 2/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 创建完整的 IFC 项目骨架（Project→Site→Building→Storey）
- **Input**: Empty or minimal IFC
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task create-ifc-project-structure <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with full project hierarchy
- **Constraint**: Must have IfcProject, IfcSite, IfcBuilding, at least 1 IfcBuildingStorey
- **Affected Classes**: IfcProject, IfcSite, IfcBuilding, IfcBuildingStorey

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenHouse generate house tutorial; buildingSMART PCERT
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
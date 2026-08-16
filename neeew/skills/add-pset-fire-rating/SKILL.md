---
name: bsr-add-pset-fire-rating
description: |-
  BSR engineering task: 为所有 IfcWall/IfcSlab 添加标准化 Pset_WallCommon.FireRating. Use when the user needs to 为所有 IfcWall/IfcSlab 添加标准化 Pset_WallCommon.FireRating in an IFC/BIM file. Applicable when the model has IFC without fire rating properties.
  TRIGGER — use whenever: the user mentions 为所有 IfcWall/IfcSlab 添加标准化 Pset_WallCommon.FireRating; the IFC contains IFC without fire rating properties; or the user asks to fix/check/rename/report related to IfcWall, IfcSlab, IfcPropertySet.
license: MIT
---

# BSR Task — add-pset-fire-rating

> Task Library: `Task025` · Difficulty 2/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 为所有 IfcWall/IfcSlab 添加标准化 Pset_WallCommon.FireRating
- **Input**: IFC without fire rating properties
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task add-pset-fire-rating <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcWall, IfcSlab, IfcPropertySet) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with FireRating on all fire-rated elements
- **Constraint**: FireRating must be 0.5HR/1HR/2HR/4HR
- **Affected Classes**: IfcWall, IfcSlab, IfcPropertySet

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell api.pset example; buildingSMART IFC4 property sets
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-set-walls-fire-rating
description: |-
  BSR engineering task: 为所有 IfcWall 添加 Pset_WallCommon.FireRating. Use when the user needs to 为所有 IfcWall 添加 Pset_WallCommon.FireRating in an IFC/BIM file. Applicable when the model has IFC with walls missing fire rating.
  TRIGGER — use whenever: the user mentions 为所有 IfcWall 添加 Pset_WallCommon.FireRating; the IFC contains IFC with walls missing fire rating; or the user asks to fix/check/rename/report related to IfcWall, IfcWallType.
license: MIT
---

# BSR Task — set-walls-fire-rating

> Task Library: `Task003` · Difficulty 2/5 · Frequency Medium · Business Value 9/10

## When to use

- **Goal**: 为所有 IfcWall 添加 Pset_WallCommon.FireRating
- **Input**: IFC with walls missing fire rating
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task set-walls-fire-rating <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcWall, IfcWallType) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with FireRating property on all walls
- **Constraint**: FireRating must be one of: 0.5HR, 1HR, 2HR, 4HR
- **Affected Classes**: IfcWall, IfcWallType

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART IFC4 property sets; fire code compliance
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
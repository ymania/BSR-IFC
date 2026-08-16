---
name: bsr-standardize-wall-types
description: |-
  BSR engineering task: 统一 IfcWall 的 IfcWallType 关联. Use when the user needs to 统一 IfcWall 的 IfcWallType 关联 in an IFC/BIM file. Applicable when the model has IFC with walls having no type assignment.
  TRIGGER — use whenever: the user mentions 统一 IfcWall 的 IfcWallType 关联; the IFC contains IFC with walls having no type assignment; or the user asks to fix/check/rename/report related to IfcWall, IfcWallType, IfcRelDefinesByType.
license: MIT
---

# BSR Task — standardize-wall-types

> Task Library: `Task002` · Difficulty 2/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 统一 IfcWall 的 IfcWallType 关联
- **Input**: IFC with walls having no type assignment
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task standardize-wall-types <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcWall, IfcWallType, IfcRelDefinesByType) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with each wall linked to a IfcWallType
- **Constraint**: All IfcWall must have IfcRelDefinesByType
- **Affected Classes**: IfcWall, IfcWallType, IfcRelDefinesByType

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell code examples; BIMTester common rules
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-rename-bridge-parts
description: |-
  BSR engineering task: 统一桥梁构件命名. Use when the user needs to 统一桥梁构件命名 in an IFC/BIM file. Applicable when the model has IFC with bridge elements named generically.
  TRIGGER — use whenever: the user mentions 统一桥梁构件命名; the IFC contains IFC with bridge elements named generically; or the user asks to fix/check/rename/report related to IfcBridge (IFC4X3), IfcBeam, IfcPile.
license: MIT
---

# BSR Task — rename-bridge-parts

> Task Library: `Task018` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 统一桥梁构件命名
- **Input**: IFC with bridge elements named generically
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task rename-bridge-parts <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcBridge (IFC4X3), IfcBeam, IfcPile) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with bridge-consistent naming (girder/abutment/pier)
- **Constraint**: Name must include structural role
- **Affected Classes**: IfcBridge (IFC4X3), IfcBeam, IfcPile

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: KIT bridge examples; planen-bauen 4.0 bridge IFC
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
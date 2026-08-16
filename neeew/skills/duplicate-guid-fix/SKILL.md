---
name: bsr-duplicate-guid-fix
description: |-
  BSR engineering task: 修复重复 GUID（已有 BSR task）. Use when the user needs to 修复重复 GUID（已有 BSR task） in an IFC/BIM file. Applicable when the model has IFC with duplicate GlobalId.
  TRIGGER — use whenever: the user mentions 修复重复 GUID（已有 BSR task）; the IFC contains IFC with duplicate GlobalId; or the user asks to fix/check/rename/report related to All entities.
license: MIT
---

# BSR Task — duplicate-guid-fix

> Task Library: `Task022` · Difficulty 1/5 · Frequency Low · Business Value 9/10

## When to use

- **Goal**: 修复重复 GUID（已有 BSR task）
- **Input**: IFC with duplicate GlobalId
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task duplicate-guid-fix <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All entities) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with all GUIDs unique
- **Constraint**: GlobalId must be unique across file
- **Affected Classes**: All entities

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell validation; buildingSMART IDs spec
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
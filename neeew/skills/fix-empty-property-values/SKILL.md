---
name: bsr-fix-empty-property-values
description: |-
  BSR engineering task: 将空 Property 值填充为默认值 N/A. Use when the user needs to 将空 Property 值填充为默认值 N/A in an IFC/BIM file. Applicable when the model has IFC with empty property values.
  TRIGGER — use whenever: the user mentions 将空 Property 值填充为默认值 N/A; the IFC contains IFC with empty property values; or the user asks to fix/check/rename/report related to All IfcPropertySingleValue.
license: MIT
---

# BSR Task — fix-empty-property-values

> Task Library: `Task037` · Difficulty 2/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 将空 Property 值填充为默认值 N/A
- **Input**: IFC with empty property values
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task fix-empty-property-values <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcPropertySingleValue) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with all property values non-empty
- **Constraint**: Empty properties should be set to N/A or —
- **Affected Classes**: All IfcPropertySingleValue

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: Revit IFC export: empty properties skipped (Issue #160); xbim workaround
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
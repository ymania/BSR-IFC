---
name: bsr-normalize-property-names
description: |-
  BSR engineering task: 统一属性集命名（消除拼写差异）. Use when the user needs to 统一属性集命名（消除拼写差异） in an IFC/BIM file. Applicable when the model has IFC with inconsistent property names.
  TRIGGER — use whenever: the user mentions 统一属性集命名（消除拼写差异）; the IFC contains IFC with inconsistent property names; or the user asks to fix/check/rename/report related to All IfcPropertySet.
license: MIT
---

# BSR Task — normalize-property-names

> Task Library: `Task021` · Difficulty 2/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 统一属性集命名（消除拼写差异）
- **Input**: IFC with inconsistent property names
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task normalize-property-names <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcPropertySet) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with standardized Pset names
- **Constraint**: Property set names must match IFC4 schema
- **Affected Classes**: All IfcPropertySet

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART validation service errors; xbim issues
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
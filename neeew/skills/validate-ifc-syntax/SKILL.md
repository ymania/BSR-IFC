---
name: bsr-validate-ifc-syntax
description: |-
  BSR engineering task: 运行 ifcopenshell.validate 语法检查. Use when the user needs to 运行 ifcopenshell.validate 语法检查 in an IFC/BIM file. Applicable when the model has Any IFC file.
  TRIGGER — use whenever: the user mentions 运行 ifcopenshell.validate 语法检查; the IFC contains Any IFC file; or the user asks to fix/check/rename/report related to All entities.
license: MIT
---

# BSR Task — validate-ifc-syntax

> Task Library: `Task024` · Difficulty 1/5 · Frequency High · Business Value 10/10

## When to use

- **Goal**: 运行 ifcopenshell.validate 语法检查
- **Input**: Any IFC file
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task validate-ifc-syntax <file.ifc>
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

- **Output**: Validation report with errors/warnings/info
- **Constraint**: Schema compliance: IFC4 or IFC2X3
- **Affected Classes**: All entities

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART validation service; IfcOpenShell validate module
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
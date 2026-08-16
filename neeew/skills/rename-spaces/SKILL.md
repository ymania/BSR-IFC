---
name: bsr-rename-spaces
description: |-
  BSR engineering task: 按楼层编号规则重命名所有 IfcSpace. Use when the user needs to 按楼层编号规则重命名所有 IfcSpace in an IFC/BIM file. Applicable when the model has IFC with unnamed/duplicate spaces.
  TRIGGER — use whenever: the user mentions 按楼层编号规则重命名所有 IfcSpace; the IFC contains IFC with unnamed/duplicate spaces; or the user asks to fix/check/rename/report related to IfcSpace, IfcBuildingStorey.
license: MIT
---

# BSR Task — rename-spaces

> Task Library: `Task001` · Difficulty 1/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 按楼层编号规则重命名所有 IfcSpace
- **Input**: IFC with unnamed/duplicate spaces
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task rename-spaces <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcBuildingStorey) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with consistent space naming
- **Constraint**: Space names must be unique per storey
- **Affected Classes**: IfcSpace, IfcBuildingStorey

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART MSG example; common BIM mandate
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
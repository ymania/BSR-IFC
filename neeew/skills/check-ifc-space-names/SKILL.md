---
name: bsr-check-ifc-space-names
description: |-
  BSR engineering task: 验证所有 IfcSpace 有非空唯一名称. Use when the user needs to 验证所有 IfcSpace 有非空唯一名称 in an IFC/BIM file. Applicable when the model has IFC with unnamed or duplicate spaces.
  TRIGGER — use whenever: the user mentions 验证所有 IfcSpace 有非空唯一名称; the IFC contains IFC with unnamed or duplicate spaces; or the user asks to fix/check/rename/report related to IfcSpace.
license: MIT
---

# BSR Task — check-ifc-space-names

> Task Library: `Task034` · Difficulty 1/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 验证所有 IfcSpace 有非空唯一名称
- **Input**: IFC with unnamed or duplicate spaces
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-ifc-space-names <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing unnamed/duplicate spaces
- **Constraint**: Each space must have unique non-empty name
- **Affected Classes**: IfcSpace

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART industry practices; IDS requirements
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
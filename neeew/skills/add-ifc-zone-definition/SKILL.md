---
name: bsr-add-ifc-zone-definition
description: |-
  BSR engineering task: 将房间按部门分组为 IfcZone. Use when the user needs to 将房间按部门分组为 IfcZone in an IFC/BIM file. Applicable when the model has IFC with IfcSpace but no IfcZone.
  TRIGGER — use whenever: the user mentions 将房间按部门分组为 IfcZone; the IFC contains IFC with IfcSpace but no IfcZone; or the user asks to fix/check/rename/report related to IfcZone, IfcSpace, IfcRelAssignsToGroup.
license: MIT
---

# BSR Task — add-ifc-zone-definition

> Task Library: `Task009` · Difficulty 3/5 · Frequency Low · Business Value 7/10

## When to use

- **Goal**: 将房间按部门分组为 IfcZone
- **Input**: IFC with IfcSpace but no IfcZone
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task add-ifc-zone-definition <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcZone, IfcSpace, IfcRelAssignsToGroup) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with zone hierarchy added
- **Constraint**: Each zone must reference existing spaces
- **Affected Classes**: IfcZone, IfcSpace, IfcRelAssignsToGroup

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART zone example; facility management
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
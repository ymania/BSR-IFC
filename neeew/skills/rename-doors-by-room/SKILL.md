---
name: bsr-rename-doors-by-room
description: |-
  BSR engineering task: 按关联房间名自动命名 IfcDoor. Use when the user needs to 按关联房间名自动命名 IfcDoor in an IFC/BIM file. Applicable when the model has IFC with doors named 'Door-001'.
  TRIGGER — use whenever: the user mentions 按关联房间名自动命名 IfcDoor; the IFC contains IFC with doors named 'Door-001'; or the user asks to fix/check/rename/report related to IfcDoor, IfcSpace, IfcRelSpaceBoundary.
license: MIT
---

# BSR Task — rename-doors-by-room

> Task Library: `Task007` · Difficulty 2/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 按关联房间名自动命名 IfcDoor
- **Input**: IFC with doors named 'Door-001'
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task rename-doors-by-room <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcDoor, IfcSpace, IfcRelSpaceBoundary) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with doors named 'R-Office-D01' pattern
- **Constraint**: Door name must include room name prefix
- **Affected Classes**: IfcDoor, IfcSpace, IfcRelSpaceBoundary

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: BIM mandate naming conventions; common handover requirement
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
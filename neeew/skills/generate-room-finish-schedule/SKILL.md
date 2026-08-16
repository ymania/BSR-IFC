---
name: bsr-generate-room-finish-schedule
description: |-
  BSR engineering task: 生成房间装修做法明细表. Use when the user needs to 生成房间装修做法明细表 in an IFC/BIM file. Applicable when the model has IFC with IfcSpace having finish properties.
  TRIGGER — use whenever: the user mentions 生成房间装修做法明细表; the IFC contains IFC with IfcSpace having finish properties; or the user asks to fix/check/rename/report related to IfcSpace, IfcRelDefinesByProperties.
license: MIT
---

# BSR Task — generate-room-finish-schedule

> Task Library: `Task006` · Difficulty 2/5 · Frequency Low · Business Value 6/10

## When to use

- **Goal**: 生成房间装修做法明细表
- **Input**: IFC with IfcSpace having finish properties
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task generate-room-finish-schedule <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcRelDefinesByProperties) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: CSV schedule with floor/wall/ceiling finish per room
- **Constraint**: Rooms without finish properties flagged as warning
- **Affected Classes**: IfcSpace, IfcRelDefinesByProperties

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: COBie requirements; facility management handover
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
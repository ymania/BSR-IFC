---
name: bsr-check-door-width-minimum
description: |-
  BSR engineering task: 检查所有 IfcDoor 宽度是否满足最小值. Use when the user needs to 检查所有 IfcDoor 宽度是否满足最小值 in an IFC/BIM file. Applicable when the model has IFC with doors.
  TRIGGER — use whenever: the user mentions 检查所有 IfcDoor 宽度是否满足最小值; the IFC contains IFC with doors; or the user asks to fix/check/rename/report related to IfcDoor, IfcQuantityLength.
license: MIT
---

# BSR Task — check-door-width-minimum

> Task Library: `Task008` · Difficulty 2/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 检查所有 IfcDoor 宽度是否满足最小值
- **Input**: IFC with doors
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-door-width-minimum <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcDoor, IfcQuantityLength) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing doors below 800mm width
- **Constraint**: Door width >= 800mm (office), >= 600mm (residential)
- **Affected Classes**: IfcDoor, IfcQuantityLength

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: building code compliance; accessibility requirements
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
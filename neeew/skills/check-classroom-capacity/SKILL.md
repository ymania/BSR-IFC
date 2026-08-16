---
name: bsr-check-classroom-capacity
description: |-
  BSR engineering task: 验证教室面积是否满足学生容量要求. Use when the user needs to 验证教室面积是否满足学生容量要求 in an IFC/BIM file. Applicable when the model has IFC with classrooms.
  TRIGGER — use whenever: the user mentions 验证教室面积是否满足学生容量要求; the IFC contains IFC with classrooms; or the user asks to fix/check/rename/report related to IfcSpace, IfcQuantityArea.
license: MIT
---

# BSR Task — check-classroom-capacity

> Task Library: `Task015` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 验证教室面积是否满足学生容量要求
- **Input**: IFC with classrooms
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-classroom-capacity <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcQuantityArea) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report marking undersized rooms
- **Constraint**: Area per student >= 1.8m²
- **Affected Classes**: IfcSpace, IfcQuantityArea

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: School design code compliance
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-check-crane-clearance
description: |-
  BSR engineering task: 检查吊车净空高度. Use when the user needs to 检查吊车净空高度 in an IFC/BIM file. Applicable when the model has IFC with industrial building and crane.
  TRIGGER — use whenever: the user mentions 检查吊车净空高度; the IFC contains IFC with industrial building and crane; or the user asks to fix/check/rename/report related to IfcCraneRail, IfcBeam, IfcColumn.
license: MIT
---

# BSR Task — check-crane-clearance

> Task Library: `Task017` · Difficulty 4/5 · Frequency Low · Business Value 7/10

## When to use

- **Goal**: 检查吊车净空高度
- **Input**: IFC with industrial building and crane
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-crane-clearance <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcCraneRail, IfcBeam, IfcColumn) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report checking crane vs structure clearance
- **Constraint**: Crane clearance >= 500mm
- **Affected Classes**: IfcCraneRail, IfcBeam, IfcColumn

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: Industrial BIM validation; KIT IFC examples
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
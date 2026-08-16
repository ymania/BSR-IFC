---
name: bsr-assign-system-to-mep
description: |-
  BSR engineering task: 将 MEP 设备分配到 IfcSystem. Use when the user needs to 将 MEP 设备分配到 IfcSystem in an IFC/BIM file. Applicable when the model has IFC with unassigned MEP elements.
  TRIGGER — use whenever: the user mentions 将 MEP 设备分配到 IfcSystem; the IFC contains IFC with unassigned MEP elements; or the user asks to fix/check/rename/report related to IfcFlowTerminal, IfcFlowSegment, IfcDistributionSystem.
license: MIT
---

# BSR Task — assign-system-to-mep

> Task Library: `Task044` · Difficulty 2/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 将 MEP 设备分配到 IfcSystem
- **Input**: IFC with unassigned MEP elements
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task assign-system-to-mep <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcFlowTerminal, IfcFlowSegment, IfcDistributionSystem) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with each MEP element in a system
- **Constraint**: Each flow element should be in IfcDistributionSystem
- **Affected Classes**: IfcFlowTerminal, IfcFlowSegment, IfcDistributionSystem

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART IFC4 MEP; system assignment
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
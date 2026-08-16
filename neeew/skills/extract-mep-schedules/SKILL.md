---
name: bsr-extract-mep-schedules
description: |-
  BSR engineering task: 提取所有 MEP 设备参数表. Use when the user needs to 提取所有 MEP 设备参数表 in an IFC/BIM file. Applicable when the model has IFC with IfcFlowTerminal/IfcFlowFitting.
  TRIGGER — use whenever: the user mentions 提取所有 MEP 设备参数表; the IFC contains IFC with IfcFlowTerminal/IfcFlowFitting; or the user asks to fix/check/rename/report related to IfcFlowTerminal, IfcFlowFitting, IfcFlowSegment.
license: MIT
---

# BSR Task — extract-mep-schedules

> Task Library: `Task010` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 提取所有 MEP 设备参数表
- **Input**: IFC with IfcFlowTerminal/IfcFlowFitting
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task extract-mep-schedules <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcFlowTerminal, IfcFlowFitting, IfcFlowSegment) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: CSV schedule with flow rates, pressure, power
- **Constraint**: N/A — read-only
- **Affected Classes**: IfcFlowTerminal, IfcFlowFitting, IfcFlowSegment

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: RWTH E3D DigitalHub HVAC dataset; MEP handover
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-check-medical-gas-zoning
description: |-
  BSR engineering task: 检查医疗气体管道分区. Use when the user needs to 检查医疗气体管道分区 in an IFC/BIM file. Applicable when the model has IFC with IfcFlowSegment for medical gas.
  TRIGGER — use whenever: the user mentions 检查医疗气体管道分区; the IFC contains IFC with IfcFlowSegment for medical gas; or the user asks to fix/check/rename/report related to IfcFlowSegment, IfcZone.
license: MIT
---

# BSR Task — check-medical-gas-zoning

> Task Library: `Task013` · Difficulty 4/5 · Frequency Low · Business Value 8/10

## When to use

- **Goal**: 检查医疗气体管道分区
- **Input**: IFC with IfcFlowSegment for medical gas
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-medical-gas-zoning <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcFlowSegment, IfcZone) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report checking zone-isolation compliance
- **Constraint**: Medical gas pipes must be zone-isolated
- **Affected Classes**: IfcFlowSegment, IfcZone

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: Hospital MEP validation; NFPA 99 compliance
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
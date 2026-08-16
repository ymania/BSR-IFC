---
name: bsr-check-duct-connectivity
description: |-
  BSR engineering task: 验证 IfcFlowSegment 连接性. Use when the user needs to 验证 IfcFlowSegment 连接性 in an IFC/BIM file. Applicable when the model has MEP IFC with disconnected ducts.
  TRIGGER — use whenever: the user mentions 验证 IfcFlowSegment 连接性; the IFC contains MEP IFC with disconnected ducts; or the user asks to fix/check/rename/report related to IfcFlowSegment, IfcFlowFitting.
license: MIT
---

# BSR Task — check-duct-connectivity

> Task Library: `Task043` · Difficulty 3/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 验证 IfcFlowSegment 连接性
- **Input**: MEP IFC with disconnected ducts
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-duct-connectivity <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcFlowSegment, IfcFlowFitting) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing disconnected segments
- **Constraint**: Each duct must be connected to at least 2 fittings or terminals
- **Affected Classes**: IfcFlowSegment, IfcFlowFitting

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: RWTH DigitalHub HVAC; MEP validation
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
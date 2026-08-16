---
name: bsr-check-beam-column-connectivity
description: |-
  BSR engineering task: 验证梁柱节点连接. Use when the user needs to 验证梁柱节点连接 in an IFC/BIM file. Applicable when the model has IFC structural model.
  TRIGGER — use whenever: the user mentions 验证梁柱节点连接; the IFC contains IFC structural model; or the user asks to fix/check/rename/report related to IfcBeam, IfcColumn, IfcRelConnectsElements.
license: MIT
---

# BSR Task — check-beam-column-connectivity

> Task Library: `Task050` · Difficulty 3/5 · Frequency Low · Business Value 7/10

## When to use

- **Goal**: 验证梁柱节点连接
- **Input**: IFC structural model
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-beam-column-connectivity <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcBeam, IfcColumn, IfcRelConnectsElements) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing disconnected beam-column joints
- **Constraint**: Each beam end must connect to a column or wall
- **Affected Classes**: IfcBeam, IfcColumn, IfcRelConnectsElements

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: KIT structural IFC examples; structural validation
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
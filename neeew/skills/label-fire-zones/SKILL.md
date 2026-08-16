---
name: bsr-label-fire-zones
description: |-
  BSR engineering task: 按防火分区为 IfcSpace 添加 FireRisk 属性. Use when the user needs to 按防火分区为 IfcSpace 添加 FireRisk 属性 in an IFC/BIM file. Applicable when the model has IFC without fire zone properties.
  TRIGGER — use whenever: the user mentions 按防火分区为 IfcSpace 添加 FireRisk 属性; the IFC contains IFC without fire zone properties; or the user asks to fix/check/rename/report related to IfcSpace, IfcZone.
license: MIT
---

# BSR Task — label-fire-zones

> Task Library: `Task016` · Difficulty 3/5 · Frequency Medium · Business Value 9/10

## When to use

- **Goal**: 按防火分区为 IfcSpace 添加 FireRisk 属性
- **Input**: IFC without fire zone properties
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task label-fire-zones <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcZone) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with FireRisk (Low/Medium/High) on spaces
- **Constraint**: Fire zones must be contiguous
- **Affected Classes**: IfcSpace, IfcZone

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: Industrial fire code; IFC property sets
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
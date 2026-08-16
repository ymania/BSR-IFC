---
name: bsr-extract-space-boundaries
description: |-
  BSR engineering task: 提取 IfcSpace 的 IfcRelSpaceBoundary 拓扑关系. Use when the user needs to 提取 IfcSpace 的 IfcRelSpaceBoundary 拓扑关系 in an IFC/BIM file. Applicable when the model has IFC with spaces.
  TRIGGER — use whenever: the user mentions 提取 IfcSpace 的 IfcRelSpaceBoundary 拓扑关系; the IFC contains IFC with spaces; or the user asks to fix/check/rename/report related to IfcSpace, IfcRelSpaceBoundary.
license: MIT
---

# BSR Task — extract-space-boundaries

> Task Library: `Task049` · Difficulty 2/5 · Frequency Low · Business Value 7/10

## When to use

- **Goal**: 提取 IfcSpace 的 IfcRelSpaceBoundary 拓扑关系
- **Input**: IFC with spaces
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task extract-space-boundaries <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcRelSpaceBoundary) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: JSON listing each room's bounding walls/doors/windows
- **Constraint**: N/A — read-only
- **Affected Classes**: IfcSpace, IfcRelSpaceBoundary

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART space boundary example; HITOS model analysis
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
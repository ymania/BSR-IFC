---
name: bsr-check-spatial-containment
description: |-
  BSR engineering task: 验证所有 IfcBuildingElement 有且仅有一个空间容器. Use when the user needs to 验证所有 IfcBuildingElement 有且仅有一个空间容器 in an IFC/BIM file. Applicable when the model has IFC with elements missing spatial containment.
  TRIGGER — use whenever: the user mentions 验证所有 IfcBuildingElement 有且仅有一个空间容器; the IFC contains IFC with elements missing spatial containment; or the user asks to fix/check/rename/report related to IfcBuildingElement, IfcRelContainedInSpatialStructure.
license: MIT
---

# BSR Task — check-spatial-containment

> Task Library: `Task030` · Difficulty 2/5 · Frequency High · Business Value 10/10

## When to use

- **Goal**: 验证所有 IfcBuildingElement 有且仅有一个空间容器
- **Input**: IFC with elements missing spatial containment
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-spatial-containment <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcBuildingElement, IfcRelContainedInSpatialStructure) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing orphan elements
- **Constraint**: Each element must be in exactly one IfcBuildingStorey
- **Affected Classes**: IfcBuildingElement, IfcRelContainedInSpatialStructure

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART SPS007; validation service gherkin rules
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
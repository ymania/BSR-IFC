---
name: bsr-fix-floating-slabs
description: |-
  BSR engineering task: 检测并修复未关联 IfcBuildingStorey 的 IfcSlab. Use when the user needs to 检测并修复未关联 IfcBuildingStorey 的 IfcSlab in an IFC/BIM file. Applicable when the model has IFC with slabs not contained in any storey.
  TRIGGER — use whenever: the user mentions 检测并修复未关联 IfcBuildingStorey 的 IfcSlab; the IFC contains IFC with slabs not contained in any storey; or the user asks to fix/check/rename/report related to IfcSlab, IfcBuildingStorey, IfcRelContainedInSpatialStructure.
license: MIT
---

# BSR Task — fix-floating-slabs

> Task Library: `Task004` · Difficulty 1/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 检测并修复未关联 IfcBuildingStorey 的 IfcSlab
- **Input**: IFC with slabs not contained in any storey
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task fix-floating-slabs <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSlab, IfcBuildingStorey, IfcRelContainedInSpatialStructure) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with all slabs in IfcRelContainedInSpatialStructure
- **Constraint**: Each IfcSlab must have exactly one container
- **Affected Classes**: IfcSlab, IfcBuildingStorey, IfcRelContainedInSpatialStructure

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: BIMTester spatial containment rules; real IFC export issues
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-assign-element-to-storey
description: |-
  BSR engineering task: 将游离元素分配到合适的楼层. Use when the user needs to 将游离元素分配到合适的楼层 in an IFC/BIM file. Applicable when the model has IFC with orphans not in any storey.
  TRIGGER — use whenever: the user mentions 将游离元素分配到合适的楼层; the IFC contains IFC with orphans not in any storey; or the user asks to fix/check/rename/report related to All IfcBuildingElement.
license: MIT
---

# BSR Task — assign-element-to-storey

> Task Library: `Task041` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 将游离元素分配到合适的楼层
- **Input**: IFC with orphans not in any storey
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task assign-element-to-storey <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcBuildingElement) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with all elements in a storey
- **Constraint**: Each element assigned to closest storey by Z
- **Affected Classes**: All IfcBuildingElement

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell spatial.assign_container; common BIM issue
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
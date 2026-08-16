---
name: bsr-add-qto-slab-quantities
description: |-
  BSR engineering task: 为 IfcSlab 添加标准量. Use when the user needs to 为 IfcSlab 添加标准量 in an IFC/BIM file. Applicable when the model has IFC slabs without quantity sets.
  TRIGGER — use whenever: the user mentions 为 IfcSlab 添加标准量; the IFC contains IFC slabs without quantity sets; or the user asks to fix/check/rename/report related to IfcSlab, IfcQuantityArea.
license: MIT
---

# BSR Task — add-qto-slab-quantities

> Task Library: `Task028` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 为 IfcSlab 添加标准量
- **Input**: IFC slabs without quantity sets
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task add-qto-slab-quantities <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSlab, IfcQuantityArea) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with Qto_SlabBaseQuantities
- **Constraint**: NetArea/NetVolume/Perimeter required
- **Affected Classes**: IfcSlab, IfcQuantityArea

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell qto example; quantity surveying
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
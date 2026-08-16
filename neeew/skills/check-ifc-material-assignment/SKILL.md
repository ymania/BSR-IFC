---
name: bsr-check-ifc-material-assignment
description: |-
  BSR engineering task: 验证所有物理元素有材质. Use when the user needs to 验证所有物理元素有材质 in an IFC/BIM file. Applicable when the model has IFC with elements missing material.
  TRIGGER — use whenever: the user mentions 验证所有物理元素有材质; the IFC contains IFC with elements missing material; or the user asks to fix/check/rename/report related to IfcWall, IfcSlab, IfcBeam, IfcColumn.
license: MIT
---

# BSR Task — check-ifc-material-assignment

> Task Library: `Task046` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 验证所有物理元素有材质
- **Input**: IFC with elements missing material
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-ifc-material-assignment <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcWall, IfcSlab, IfcBeam, IfcColumn) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing non-material elements
- **Constraint**: Each physical element should have IfcMaterial
- **Affected Classes**: IfcWall, IfcSlab, IfcBeam, IfcColumn

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: BIMTester common rules; material passport
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
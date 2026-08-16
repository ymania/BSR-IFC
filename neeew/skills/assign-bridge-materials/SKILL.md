---
name: bsr-assign-bridge-materials
description: |-
  BSR engineering task: 为 IfcBeam/IfcPile 添加材质属性. Use when the user needs to 为 IfcBeam/IfcPile 添加材质属性 in an IFC/BIM file. Applicable when the model has Bridge IFC missing material assignment.
  TRIGGER — use whenever: the user mentions 为 IfcBeam/IfcPile 添加材质属性; the IFC contains Bridge IFC missing material assignment; or the user asks to fix/check/rename/report related to IfcBeam, IfcPile, IfcMaterial.
license: MIT
---

# BSR Task — assign-bridge-materials

> Task Library: `Task019` · Difficulty 2/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 为 IfcBeam/IfcPile 添加材质属性
- **Input**: Bridge IFC missing material assignment
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task assign-bridge-materials <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcBeam, IfcPile, IfcMaterial) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with material on all structural elements
- **Constraint**: Each structural element must have IfcMaterial
- **Affected Classes**: IfcBeam, IfcPile, IfcMaterial

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART IFC4X3 bridge extension; material passport
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
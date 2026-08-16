---
name: bsr-classify-hospital-rooms
description: |-
  BSR engineering task: 按医技科室分类 IfcSpace 并添加属性. Use when the user needs to 按医技科室分类 IfcSpace 并添加属性 in an IFC/BIM file. Applicable when the model has IFC with generic IfcSpace.
  TRIGGER — use whenever: the user mentions 按医技科室分类 IfcSpace 并添加属性; the IFC contains IFC with generic IfcSpace; or the user asks to fix/check/rename/report related to IfcSpace, IfcClassification.
license: MIT
---

# BSR Task — classify-hospital-rooms

> Task Library: `Task012` · Difficulty 3/5 · Frequency Low · Business Value 9/10

## When to use

- **Goal**: 按医技科室分类 IfcSpace 并添加属性
- **Input**: IFC with generic IfcSpace
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task classify-hospital-rooms <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcClassification) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with spaces classified as OR/ICU/ward/lab/pharmacy
- **Constraint**: Classification must match predefined hospital room types
- **Affected Classes**: IfcSpace, IfcClassification

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: HITOS hospital IFC model; healthcare BIM standards
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
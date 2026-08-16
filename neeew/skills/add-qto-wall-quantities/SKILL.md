---
name: bsr-add-qto-wall-quantities
description: |-
  BSR engineering task: 为 IfcWall 添加标准面积/体积/长度量. Use when the user needs to 为 IfcWall 添加标准面积/体积/长度量 in an IFC/BIM file. Applicable when the model has IFC walls without quantity take-off data.
  TRIGGER — use whenever: the user mentions 为 IfcWall 添加标准面积/体积/长度量; the IFC contains IFC walls without quantity take-off data; or the user asks to fix/check/rename/report related to IfcWall, IfcQuantityArea, IfcQuantityLength.
license: MIT
---

# BSR Task — add-qto-wall-quantities

> Task Library: `Task027` · Difficulty 2/5 · Frequency Medium · Business Value 8/10

## When to use

- **Goal**: 为 IfcWall 添加标准面积/体积/长度量
- **Input**: IFC walls without quantity take-off data
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task add-qto-wall-quantities <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcWall, IfcQuantityArea, IfcQuantityLength) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with Qto_WallBaseQuantities populated
- **Constraint**: Quantities must have valid measure values
- **Affected Classes**: IfcWall, IfcQuantityArea, IfcQuantityLength

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell api.pset.add_qto; QTO standard
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
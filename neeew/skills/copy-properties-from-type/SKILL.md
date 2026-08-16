---
name: bsr-copy-properties-from-type
description: |-
  BSR engineering task: 将 IfcType 的属性复制到所有实例. Use when the user needs to 将 IfcType 的属性复制到所有实例 in an IFC/BIM file. Applicable when the model has IFC with properties only on type, not instances.
  TRIGGER — use whenever: the user mentions 将 IfcType 的属性复制到所有实例; the IFC contains IFC with properties only on type, not instances; or the user asks to fix/check/rename/report related to All IfcElement, IfcType.
license: MIT
---

# BSR Task — copy-properties-from-type

> Task Library: `Task029` · Difficulty 3/5 · Frequency Medium · Business Value 7/10

## When to use

- **Goal**: 将 IfcType 的属性复制到所有实例
- **Input**: IFC with properties only on type, not instances
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task copy-properties-from-type <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcElement, IfcType) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC where each instance inherits type properties
- **Constraint**: Instance properties must not conflict with type
- **Affected Classes**: All IfcElement, IfcType

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: xbim issue: type properties not exporting to IFC; Revit export workaround
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
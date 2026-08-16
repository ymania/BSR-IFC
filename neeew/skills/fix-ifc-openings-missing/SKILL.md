---
name: bsr-fix-ifc-openings-missing
description: |-
  BSR engineering task: 检测门窗开口未正确关联 IfcOpeningElement 的缺陷. Use when the user needs to 检测门窗开口未正确关联 IfcOpeningElement 的缺陷 in an IFC/BIM file. Applicable when the model has IFC with doors/windows but no opening elements.
  TRIGGER — use whenever: the user mentions 检测门窗开口未正确关联 IfcOpeningElement 的缺陷; the IFC contains IFC with doors/windows but no opening elements; or the user asks to fix/check/rename/report related to IfcDoor, IfcWindow, IfcOpeningElement, IfcRelVoidsElement.
license: MIT
---

# BSR Task — fix-ifc-openings-missing

> Task Library: `Task020` · Difficulty 2/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 检测门窗开口未正确关联 IfcOpeningElement 的缺陷
- **Input**: IFC with doors/windows but no opening elements
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task fix-ifc-openings-missing <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcDoor, IfcWindow, IfcOpeningElement, IfcRelVoidsElement) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with IfcRelVoidsElement linking openings
- **Constraint**: Each IfcDoor/IfcWindow must have a corresponding IfcOpeningElement
- **Affected Classes**: IfcDoor, IfcWindow, IfcOpeningElement, IfcRelVoidsElement

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: BIMTester rule; common Revit IFC export issue
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
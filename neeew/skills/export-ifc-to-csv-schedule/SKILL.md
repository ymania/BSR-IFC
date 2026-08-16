---
name: bsr-export-ifc-to-csv-schedule
description: |-
  BSR engineering task: 将 IFC 构件数量/类型/属性导出为 CSV. Use when the user needs to 将 IFC 构件数量/类型/属性导出为 CSV in an IFC/BIM file. Applicable when the model has Any IFC file.
  TRIGGER — use whenever: the user mentions 将 IFC 构件数量/类型/属性导出为 CSV; the IFC contains Any IFC file; or the user asks to fix/check/rename/report related to All IfcBuildingElement.
license: MIT
---

# BSR Task — export-ifc-to-csv-schedule

> Task Library: `Task023` · Difficulty 1/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 将 IFC 构件数量/类型/属性导出为 CSV
- **Input**: Any IFC file
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task export-ifc-to-csv-schedule <file.ifc>
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

- **Output**: CSV file with element count, type, property summary
- **Constraint**: N/A — export only
- **Affected Classes**: All IfcBuildingElement

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcCSV tool; common quantity surveyor request
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
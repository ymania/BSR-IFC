---
name: bsr-count-spaces-by-floor
description: |-
  BSR engineering task: 按楼层统计 IfcSpace 数量并输出表格. Use when the user needs to 按楼层统计 IfcSpace 数量并输出表格 in an IFC/BIM file. Applicable when the model has IFC with spaces.
  TRIGGER — use whenever: the user mentions 按楼层统计 IfcSpace 数量并输出表格; the IFC contains IFC with spaces; or the user asks to fix/check/rename/report related to IfcSpace, IfcBuildingStorey.
license: MIT
---

# BSR Task — count-spaces-by-floor

> Task Library: `Task005` · Difficulty 1/5 · Frequency High · Business Value 7/10

## When to use

- **Goal**: 按楼层统计 IfcSpace 数量并输出表格
- **Input**: IFC with spaces
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task count-spaces-by-floor <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (IfcSpace, IfcBuildingStorey) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: CSV table with floor name, space count, area sum
- **Constraint**: N/A — read-only query
- **Affected Classes**: IfcSpace, IfcBuildingStorey

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: Open IFC Model Repository analysis; quantity surveying
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-export-element-tree
description: |-
  BSR engineering task: 导出 IFC 实体树（父子关系嵌套层级）. Use when the user needs to 导出 IFC 实体树（父子关系嵌套层级） in an IFC/BIM file. Applicable when the model has Any IFC file.
  TRIGGER — use whenever: the user mentions 导出 IFC 实体树（父子关系嵌套层级）; the IFC contains Any IFC file; or the user asks to fix/check/rename/report related to All entities.
license: MIT
---

# BSR Task — export-element-tree

> Task Library: `Task047` · Difficulty 2/5 · Frequency Low · Business Value 7/10

## When to use

- **Goal**: 导出 IFC 实体树（父子关系嵌套层级）
- **Input**: Any IFC file
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task export-element-tree <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All entities) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: JSON tree of spatial containment hierarchy
- **Constraint**: N/A — export only
- **Affected Classes**: All entities

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell traverse() example; entity tree visualization
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
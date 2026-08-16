---
name: bsr-auto-name-classrooms
description: |-
  BSR engineering task: 将教学楼 IfcSpace 按'楼号-楼层-编号'规则重命名. Use when the user needs to 将教学楼 IfcSpace 按'楼号-楼层-编号'规则重命名 in an IFC/BIM file. Applicable when the model has IFC with school spaces named 'Room'.
  TRIGGER — use whenever: the user mentions 将教学楼 IfcSpace 按'楼号-楼层-编号'规则重命名; the IFC contains IFC with school spaces named 'Room'; or the user asks to fix/check/rename/report related to IfcSpace, IfcBuildingStorey.
license: MIT
---

# BSR Task — auto-name-classrooms

> Task Library: `Task014` · Difficulty 1/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 将教学楼 IfcSpace 按'楼号-楼层-编号'规则重命名
- **Input**: IFC with school spaces named 'Room'
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task auto-name-classrooms <file.ifc>
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

- **Output**: IFC with spaces named 'A-1-01' pattern
- **Constraint**: Name must match regex: ^[A-Z]-\d+-\d{2}$
- **Affected Classes**: IfcSpace, IfcBuildingStorey

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART school example; education BIM mandate
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
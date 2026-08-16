---
name: bsr-check-ifc-object-names
description: |-
  BSR engineering task: 验证所有 IfcBuildingElement 有名称. Use when the user needs to 验证所有 IfcBuildingElement 有名称 in an IFC/BIM file. Applicable when the model has IFC with unnamed elements.
  TRIGGER — use whenever: the user mentions 验证所有 IfcBuildingElement 有名称; the IFC contains IFC with unnamed elements; or the user asks to fix/check/rename/report related to All IfcBuildingElement.
license: MIT
---

# BSR Task — check-ifc-object-names

> Task Library: `Task035` · Difficulty 1/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 验证所有 IfcBuildingElement 有名称
- **Input**: IFC with unnamed elements
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-ifc-object-names <file.ifc>
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

- **Output**: Report listing unnamed elements
- **Constraint**: Each element should have descriptive name
- **Affected Classes**: All IfcBuildingElement

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART common practice checks; BIMTester
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
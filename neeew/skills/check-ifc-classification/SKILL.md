---
name: bsr-check-ifc-classification
description: |-
  BSR engineering task: 验证元素是否有 IfcClassification 关联. Use when the user needs to 验证元素是否有 IfcClassification 关联 in an IFC/BIM file. Applicable when the model has IFC without classification.
  TRIGGER — use whenever: the user mentions 验证元素是否有 IfcClassification 关联; the IFC contains IFC without classification; or the user asks to fix/check/rename/report related to All IfcElement.
license: MIT
---

# BSR Task — check-ifc-classification

> Task Library: `Task036` · Difficulty 2/5 · Frequency High · Business Value 8/10

## When to use

- **Goal**: 验证元素是否有 IfcClassification 关联
- **Input**: IFC without classification
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-ifc-classification <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcElement) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Report listing unclassified elements
- **Constraint**: Each element should have at least one classification
- **Affected Classes**: All IfcElement

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART bSDD compliance; classification standards
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
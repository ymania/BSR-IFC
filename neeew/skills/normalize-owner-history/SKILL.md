---
name: bsr-normalize-owner-history
description: |-
  BSR engineering task: 统一设置所有实体的 IfcOwnerHistory. Use when the user needs to 统一设置所有实体的 IfcOwnerHistory in an IFC/BIM file. Applicable when the model has IFC with inconsistent owner info.
  TRIGGER — use whenever: the user mentions 统一设置所有实体的 IfcOwnerHistory; the IFC contains IFC with inconsistent owner info; or the user asks to fix/check/rename/report related to All entities.
license: MIT
---

# BSR Task — normalize-owner-history

> Task Library: `Task033` · Difficulty 2/5 · Frequency Low · Business Value 6/10

## When to use

- **Goal**: 统一设置所有实体的 IfcOwnerHistory
- **Input**: IFC with inconsistent owner info
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task normalize-owner-history <file.ifc>
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

- **Output**: IFC with uniform owner history
- **Constraint**: All entities must have populated OwnerHistory
- **Affected Classes**: All entities

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART ownership compliance; implementer agreements
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
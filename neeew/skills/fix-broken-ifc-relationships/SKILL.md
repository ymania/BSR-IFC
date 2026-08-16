---
name: bsr-fix-broken-ifc-relationships
description: |-
  BSR engineering task: 检测并修复悬空的关系引用. Use when the user needs to 检测并修复悬空的关系引用 in an IFC/BIM file. Applicable when the model has IFC with relationships pointing to deleted entities.
  TRIGGER — use whenever: the user mentions 检测并修复悬空的关系引用; the IFC contains IFC with relationships pointing to deleted entities; or the user asks to fix/check/rename/report related to All IfcRelationship.
license: MIT
---

# BSR Task — fix-broken-ifc-relationships

> Task Library: `Task038` · Difficulty 3/5 · Frequency High · Business Value 9/10

## When to use

- **Goal**: 检测并修复悬空的关系引用
- **Input**: IFC with relationships pointing to deleted entities
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task fix-broken-ifc-relationships <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (All IfcRelationship) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: IFC with clean relationship graph
- **Constraint**: All IfcRel* must reference existing entities
- **Affected Classes**: All IfcRelationship

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: xbim common issues; buildingSMART reference integrity
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
---
name: bsr-check-reverse-attributes
description: |-
  BSR engineering task: 验证 IfcRel 的反向属性完整性. Use when the user needs to 验证 IfcRel 的反向属性完整性 in an IFC/BIM file. Applicable when the model has IFC with relationships.
  TRIGGER — use whenever: the user mentions 验证 IfcRel 的反向属性完整性; the IFC contains IFC with relationships; or the user asks to fix/check/rename/report related to All IfcRelationship.
license: MIT
---

# BSR Task — check-reverse-attributes

> Task Library: `Task048` · Difficulty 3/5 · Frequency Low · Business Value 6/10

## When to use

- **Goal**: 验证 IfcRel 的反向属性完整性
- **Input**: IFC with relationships
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-reverse-attributes <file.ifc>
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

- **Output**: Report checking inverse attributes
- **Constraint**: All IfcRelationship must have valid inverses
- **Affected Classes**: All IfcRelationship

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: IfcOpenShell schema querying; inverse attribute validation
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
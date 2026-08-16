---
name: bsr-check-ifc-class-not-abstract
description: |-
  BSR engineering task: 验证没有实例化抽象实体. Use when the user needs to 验证没有实例化抽象实体 in an IFC/BIM file. Applicable when the model has IFC with abstract entity instances.
  TRIGGER — use whenever: the user mentions 验证没有实例化抽象实体; the IFC contains IFC with abstract entity instances; or the user asks to fix/check/rename/report related to All entities.
license: MIT
---

# BSR Task — check-ifc-class-not-abstract

> Task Library: `Task032` · Difficulty 2/5 · Frequency Medium · Business Value 9/10

## When to use

- **Goal**: 验证没有实例化抽象实体
- **Input**: IFC with abstract entity instances
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task check-ifc-class-not-abstract <file.ifc>
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

- **Output**: Report listing abstract violations
- **Constraint**: No abstract IfcObject classes must be instantiated
- **Affected Classes**: All entities

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART validation service; EXPRESS schema rules
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
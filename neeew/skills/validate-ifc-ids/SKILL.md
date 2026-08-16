---
name: bsr-validate-ifc-ids
description: |-
  BSR engineering task: 根据 IDS (Information Delivery Specification) 文件验证 IFC. Use when the user needs to 根据 IDS (Information Delivery Specification) 文件验证 IFC in an IFC/BIM file. Applicable when the model has IFC file + IDS spec file.
  TRIGGER — use whenever: the user mentions 根据 IDS (Information Delivery Specification) 文件验证 IFC; the IFC contains IFC file + IDS spec file; or the user asks to fix/check/rename/report related to As defined in IDS.
license: MIT
---

# BSR Task — validate-ifc-ids

> Task Library: `Task045` · Difficulty 3/5 · Frequency High · Business Value 10/10

## When to use

- **Goal**: 根据 IDS (Information Delivery Specification) 文件验证 IFC
- **Input**: IFC file + IDS spec file
- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.

## How to run

```bash
bsr task validate-ifc-ids <file.ifc>
```

### Parameters

| Flag | Purpose |
|------|---------|
| `--proto` | PROTECTED mode (requires human confirmation) |

### Pre-check (read-only, always safe)

```bash
bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes (As defined in IDS) 是否存在
bsr check <file.ifc>        # 确认当前合规状态，作为 baseline
```

### Output contract

- **Output**: Compliance report per IDS requirement
- **Constraint**: All IDS requirements must pass
- **Affected Classes**: As defined in IDS

## Verification

After running, verify:

```bash
bsr check <file.ifc>        # 无新增 FAIL
bsr log <file.ifc>          # 修改已记录
bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期
```

## Notes

- Source: buildingSMART IDS; IfcTester validation; BIMTester rules
- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。
- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。
# Aider — Diff + History + 知道哪些文件

> 学习笔记 · BSR docs/studies/aider/
> 2026-07-10

## 学什么

Aider 不是一个聊天工具。Aider 是一个**文件级别的状态管理工具**，外面包了一层 LLM。

它的核心能力：

1. **Diff** — 每次修改后生成 git diff 级别的变更记录
2. **History** — 完整对话历史，可回溯、可回滚
3. **知道哪些文件** — 不是"整个项目"，而是"这次修改涉及的 N 个文件"

## BSR 能抄什么

| Aider 能力 | BSR 对应 |
|------------|----------|
| git diff → 代码变更 | `ifc_diff()` → 结构化 IFC 差异 |
| /undo → 回滚上一步 | `rollback_to_snapshot()` → 回滚到指定快照 |
| /drop → 丢弃当前对话 | `abort_tx()` → 回滚事务 |
| 自动 git commit → 记录 | `store.record_change()` + tx → 自动历史 |
| 知道改了多少文件、哪些文件 | `OperationResult.affected_ids` + `Diff.summary` |

## BSR 还没做到但 Aider 有的

1. **自动 git commit 的时机** — Aider 每次 LLM 修改后自动 commit。BSR 的 executor.execute() 已经记录 history，但 `bsr set` 没有默认给每次操作建 snapshot。可以加 `auto_snapshot` 参数。
2. **对话即历史** — Aider 的聊天历史 = 项目修改历史。BSR 的 agent_prompt 字段已经记录了自然语言指令，但没有 CLI 命令查看"这次操作对应的指令是什么"。`bsr log` 可以加一列显示指令摘要。
3. **知道改了多少文件（有数字）** — Aider 每次输出 "5 files changed, +120/-30 lines"。BSR 的 `diff` summary 输出这个，但 `bsr set` 成功后不输出。可以加。

## 不想抄的

- **自动 stage + commit** — BSR 的 Transaction 模式更干净。用户明确 begin → ops → commit/abort，而不是自动 commit。
- **回复全文带 diff** — Aider 每次回复末尾嵌完整 diff，对话一长 tokens 爆炸。BSR 让用户通过 `bsr diff` 显式查询。

## 在 BSR 里已经实现的点

Aider 的 `--diff-map-only` 模式只输出 diff 不修改文件。BSR 的 `bsr diff a.ifc b.ifc` 做的是同一件事——pure diff，无副作用。

## 参考

- https://aider.chat/
- Aider 的 repo map 技术：https://aider.chat/docs/repomap.html

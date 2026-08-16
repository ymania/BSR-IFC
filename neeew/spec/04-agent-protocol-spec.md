# BSR Agent Protocol Spec v0.2

> **Agent 如何与 BSR 通信。**
> 定义自然语言→操作的翻译协议，并保证 Agent 调用 BSR 的过程本身可恢复（集成 aads）。

---

## 协议分层

```
自然语言指令
   ↓ 意图识别（Layer A）
Task 路由（Task Planner → Task Library）
   ↓ 规划（Layer B）
Operation 序列（spec/01 原语）
   ↓ 执行（Layer C）
Constraint 复核（spec/02）→ History 记录（spec/03）
   ↓ 结果反馈
结构化 JSON → Agent（失败可重试）
```

协议层三大核心问题及其落点：

| 问题 | 落点 | 状态 |
|------|------|------|
| 1. 意图识别：自然语言 → Operation | Task Planner + Task Library（planner/router.py） | 规划中 |
| 2. 多步规划：Plan 层 | planner/ 扩展，配合 Optimizer（spec/05）自动重试 | 规划中 |
| 3. 失败反馈与重试 | 结构化 ConstraintResult（spec/02）→ Agent 修正后重试 | 已定义 |

---

## 当前通信模式（过渡方案，v0.1 保留）

```
Agent → bsr constrain --proto  path/to/file.ifc
Agent → bsr info path/to/file.ifc
Agent → Python: BSRExecutor.execute(operation)
```

所有约束检查结果以结构化 JSON 返回。

---

## aads 集成（v0.2 新增）

**目标**：任何 Agent 调用 BSR 的会话可 `track / resume / rollback`——与 BSR 对建筑数据的承诺一致。

### 集成方式

aads 的 snapshot schema（Mission/Task/Tool 三层）作为本协议的状态记录实现：

```
Agent 会话（Hermes / Claude Code / GPT …）
   ↓ aads track（Mission=用户目标, Task=BSR 任务, Tool=每次 Operation）
BSR 执行（Operation → Constraint → History）
   ↓ aads resume --json
新会话/新 Agent 无缝接续（含 BSR commit 位置、未完成 Task、漂移检测）
```

### 映射

| aads 层 | 内容 | 来源 |
|---------|------|------|
| Mission | goal / intent / acceptance criteria | 用户自然语言目标 |
| Task | phase / status / next_actions / blocker | BSR Task（task-library） |
| Tool | action / tool_name / exit_code / error | 每次 Operation 执行结果 |

### 验收标准

1. Agent 执行 BSR 任务中断（kill -9）后，`aads checkin + resume --json` 可无重分析接续；
2. 换 Agent（Hermes → 其他）不丢失 BSR 状态；
3. 外部篡改 IFC 文件时，`aads checkpoint verify` 在继续前检测漂移。

---

## 下一步（按 spec/00 收敛节奏）

- [ ] planner/router.py 打通 Task Library 路由（意图识别 v1）
- [ ] aads snapshot schema 冻结为 spec/04 的参考实现
- [ ] 定义 `bsr agent-resume` CLI：给定 aads session，恢复 BSR 上下文

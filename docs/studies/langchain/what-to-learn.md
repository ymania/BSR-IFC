# LangChain — 学什么、不学什么

> 学习笔记 · BSR docs/studies/langchain/
> 2026-07-11

## LangChain 是什么

LangChain 是一个 LLM 应用开发框架。它解决的问题是：让开发者用标准接口调用不同 LLM、组合 Prompt、管理 Chain。

它本身不是一个 Agent 框架——但 LangGraph（它的子项目）是。

## 学什么

### 1. Chain → Graph 的演进

LangChain 一开始的模型是 Chain（线性链）：A → B → C，每步依次执行。
后来发现 Agent 需要更复杂的控制流，于是有了 LangGraph（图模型）：节点可分支、可循环、可并行。

**BSR 能抄的**：Task 的演进路径和这个相同。
当前：Operation 链式执行（ModifyProperty → Check → Record）。
未来：Task 内部是 DAG（检查 → 修改 → 验证 → 记录，多分支并行）。

### 2. 统一的接口抽象

LangChain 的核心价值是 `BaseLanguageModel`、`BaseRetriever`、`BaseTool` 这些抽象层——换模型、换工具不换代码。

**BSR 能抄的**：`Operation` 已经是一个抽象层。`ConstraintRule` 也是（只需实现 `check(model)`）。Task 也应该有统一接口（`TaskInput → TaskReport`），让 Planner 可以统一路由。

### 3. LangSmith 的调试能力

LangSmith 不是框架，是观测平台。每步 LLM 调用都可追踪、可回放。

**BSR 已经有的**：`HistoryStore` 记录每次 change，`bsr log` 可查，`bsr diff` 可对比。
**BSR 还没做到的**：没有"回放"模式——把历史 change 逐条重演以复现 bug。

## 不学什么

| 不学 | 理由 |
|------|------|
| LangChain 的 Prompt 管理 | BSR 不依赖 LLM，Task 写死操作逻辑 |
| LangChain 的 Tool 注册系统 | BSR 的 Operation 数量极少且固定，不需要动态注册 |
| LangGraph 的 StateGraph 运行时 | BSR 的 state 是 IFC 文件本身，不是 dict。Pregel 模型对 BIM 场景太重 |
| LangSmith 的 LLM 追踪 | BSR 追踪的是 IFC 数据变更，不是 token 消耗 |

## LangChain 教了 BSR 什么

LangChain 对 Agent 生态最大的贡献不是代码，是**分层抽象**：
- 模型层（Model）不关心下游
- 工具层（Tool）不关心模型
- 链层（Chain）不关心工具实现
- 图层（Graph）不关心链的实现

BSR 的分层：
- IFC 文件（数据层）
- Operation（指令层）
- Constraint（校验层）
- History（状态层）
- Task（工程语义层）

每层向上提供接口，向下不依赖实现。这个分层思想抄自 LangChain，但 BSR 的领域是 building，不是 LLM。

## 一句话

LangChain 教了行业：**框架的价值不在功能数量，在抽象层的正确性。**
BSR 不需要抄 LangChain 的代码。BSR 需要抄它的**分层架构思维**——让每一层只关心自己的事，不向下泄漏实现细节。

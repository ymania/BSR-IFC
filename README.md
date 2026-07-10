# BSR — Building State Runtime

> IFC 数据的运行时层。像 Aider 操作代码一样操作 IFC 数据。

## 一句话

不卖 Agent，不卖 UI，卖一个 IFC 数据的操作规范 + 约束引擎 + 版本管理基础设施。Agent 只是这个基础设施的调用者。

## 项目结构

```
bsr/
├── spec/                    # 协议层规范（宪法）
│   ├── 01-ifc-operation-spec.md
│   ├── 02-constraint-spec.md
│   ├── 03-history-spec.md
│   └── 04-agent-protocol.md
│
├── bsr_core/               # 运行时实现
│   ├── operation/           # 操作原语（ISA）
│   │   ├── select.py
│   │   ├── create.py
│   │   ├── modify.py
│   │   ├── delete.py
│   │   └── executor.py     # 操作调度器
│   ├── constraint/          # 约束引擎
│   │   ├── engine.py        # 规则引擎入口
│   │   ├── geometric.py     # 几何约束
│   │   ├── topological.py   # 拓扑约束
│   │   ├── semantic.py      # 语义约束
│   │   └── rules.py         # 内置规则集
│   ├── history/             # 版本管理
│   │   ├── snapshot.py      # 快照
│   │   ├── change.py        # 增量变更
│   │   ├── rollback.py      # 回滚
│   │   └── diff.py          # IFC Diff
│   └── protocol/            # Agent 协议
│       ├── handler.py       # 请求调度
│       ├── plan.py          # 规划层
│       └── verify.py        # 校验层
│
├── cli/                    # 命令行
│   └── main.py             # bsr 命令入口
│
├── tests/
│   ├── fixtures/           # 测试用 IFC 文件
│   └── unit/
│
├── examples/               # 使用示例
├── docs/                   # 开发者文档
│
├── pyproject.toml
├── README.md
└── .gitignore
```

## 四层架构（规范层 → 实现层 → CLI层 → Agent层）

```
                    ┌──────────────────────┐
                    │    Agent (任何 LLM)   │
                    └────────┬─────────────┘
                             │ 04 Agent Protocol
                    ┌────────▼─────────────┐
                    │    BSR CLI / SDK      │
                    └────────┬─────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐
│ 01 Operation    │ │02 Constraint │ │ 03 History      │
│ (IFC ISA)       │ │ (Rule Engine)│ │ (Version + WAL) │
└────────┬────────┘ └──────┬───────┘ └────────┬────────┘
         │                 │                  │
         └─────────────────┼──────────────────┘
                           ▼
                    ┌──────────────┐
                    │ IFC 文件系统  │
                    └──────────────┘
```

## 当前状态

- [x] 2026-07-10 最小验证跑通（读 IFC → 改 Depth → 写回 → Schema 验证 → 几何检查 → 领域约束）
- [ ] 四份规范定稿
- [ ] 约束引擎原型
- [ ] 版本管理实现
- [ ] CLI 入口

## 命名

BSR = Building State Runtime

| 比喻 | BSR |
|------|-----|
| 对应计算机 | Operating System |
| IFC = 文件系统 | 数据层 |
| Operation Spec = ISA | 指令集 |
| Constraint = Type System | 类型检查 |
| History = Git + WAL | 版本管理 |
| Agent Protocol = OS Syscall | 系统调用 |

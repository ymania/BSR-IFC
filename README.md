# BSR — Building State Runtime

> IFC 数据的运行时层。像 Aider 操作代码一样操作 IFC 数据。

## 一句话

不卖 Agent，不卖 UI，卖一个 IFC 数据的操作规范 + 约束引擎 + 版本管理基础设施。Agent 只是这个基础设施的调用者。

产品目标：**一个真实工程人员，一句话能完成过去需要半天到一天的工作。**

## 安装

```bash
pip install ifcopenshell click
git clone git@github.com:ymania/bsr.git
cd bsr && chmod +x bsr
```

## 快速开始

```bash
# 看一个 IFC 文件长什么样
./bsr inspect building.ifc

# 合规检查
./bsr check building.ifc

# 自然语言修改
./bsr set building.ifc "把 #37 的 Depth 改成 4.0"

# 参数化修改
./bsr set building.ifc element=#37 depth=4.0

# 工程任务
./bsr task rename-room building.ifc --prefix Room-

# 看改了啥
./bsr log building.ifc
./bsr diff building.ifc building_modified.ifc

# 项目状态
./bsr status building.ifc
```

## 项目结构

```
bsr/
├── CONSTITUTION.md              # 16 条项目宪法
├── core/                        # Runtime
│   ├── constraint/              # 约束引擎（36条规则，按类型分阈值）
│   ├── history/                 # 状态记录（Transaction + Snapshot + Rollback + Diff）
│   └── operation/               # 操作执行器
├── tasks/                       # Task Library（工程任务）
│   ├── naming/rename_room.py
│   └── fire/fix_guid.py
├── planner/router.py            # 任务路由
├── cli/main.py                  # 终端入口
├── spec/                        # 四份协议文档
├── docs/studies/                # 标杆产品学习笔记
├── plugins/                     # Revit/Rhino/Blender 入口（占位）
├── examples/                    # 真实 IFC 测试文件
└── pyproject.toml
```

## 五阶段成熟度

| 阶段 | 名称 | BSR 状态 |
|------|------|----------|
| Stage 1 | 工具（Tool） | ✅ bsr exec / diff / inspect |
| Stage 2 | 助手（Assistant） | ✅ bsr chat "把 building 改成 4m" |
| Stage 3 | 顾问（Consultant） | ⬜ Task: check-fire, check-lod |
| Stage 4 | Planner（规划者） | ⬜ 自动拆解任务 |
| Stage 5 | Partner（真正的 Agent） | ⬜ 一句话完成工程整改 |

当前处于 Stage 2→3 过渡。核心 Runtime 已就绪，重心是 Task Library。

## 长期架构

```
User Goal ("让这个模型满足消防规范")
        ↓
Goal Interpreter
        ↓
Task Planner
        ↓
Building State Runtime (BSR)  ← 核心壁垒
    ┌────────┬────────┬────────┐
    ▼        ▼        ▼
Operation  Constraint  History
    │        │        │
    └────────┴────────┘
            ▼
           IFC
```

## 设计原则

1. **Runtime 不依赖 LLM** — LLM 可换、Planner 可升级，但状态管理、约束验证、历史追踪必须扎实
2. **Task 不是 Operation** — 单位是工程任务（消防整改），不是 ModifyProperty
3. **Desired State** — 用户描述最终状态，系统自己收敛（如 Kubernetes）
4. **可追踪、可验证、可恢复** — 企业放心使用

## 学习对象

- **GitHub Copilot** — 一直知道当前 Context
- **Aider** — Diff + History + 知道哪些文件
- **Cursor** — 不是聊天，是 Project
- **Kubernetes / Terraform** — Desired State

学习笔记在 `docs/studies/`。

## 当前状态（2026-07-10）

- [x] Core Runtime: Operation + Constraint(36) + History(Transaction/Snapshot/Rollback/Diff)
- [x] CLI: inspect / check / set / log / diff / task
- [x] Protocol: 自然语言 → Operation 解析器
- [x] Tasks: rename-room, fix-guid
- [x] Task Planner: 路由表
- [x] Spec: 四份协议文档
- [x] Constitution: 16 条项目宪法
- [ ] Daily Task: 每天一个新 Task
- [ ] 真实 IFC 用例收集

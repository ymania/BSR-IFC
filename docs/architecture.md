# 架构

## 分层

```
User Goal ("让这个模型满足消防规范")
        ↓
Goal Interpreter
        ↓
Task Planner
        ↓
Building State Runtime (BSR)  ← 核心
    ┌────────┬────────┬────────┐
    ▼        ▼        ▼
Operation  Constraint  History
    │        │        │
    └────────┴────────┘
            ▼
           IFC
```

## 核心模块

| 模块 | 职责 | 不做什么 |
|------|------|---------|
| Operation | 执行原子 IFC 修改（改属性、增删构件） | 不判断"能不能改" |
| Constraint | 校验修改后模型是否符合规范（36 条规则） | 不主动修改 |
| History | 事务/Snapshot/Diff/Rollback | 不做业务判断 |

## 原则

1. Runtime 不依赖 LLM — LLM 可换，状态管理不可换
2. Task ≠ Operation — 单位是"消防整改"，不是 ModifyProperty
3. Desired State — 用户说终态，系统收敛
4. 可追踪、可验证、可恢复

## 学习对象

| 产品 | 学什么 |
|------|--------|
| GitHub Copilot | 始终感知当前上下文的意识 |
| Aider | Diff + History + 知道哪些文件改了 |
| Cursor | 它是项目，不是聊天窗口 |
| Kubernetes / Terraform | Desired State — 描述终态，系统收敛 |

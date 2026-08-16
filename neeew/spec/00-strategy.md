# BSR 收敛战略 Spec v0.1

> **一个产品，一条主线。**
> 定义 BSR 在多个仓库之间的唯一身份与边界，终止并行演化造成的方向模糊。

---

## 背景：为什么写这份 Spec

截至 2026-07，ymania 名下 6 个仓库中，有 4 个在演化的不同阶段承担着"BSR"这个名字或职责：

| 仓库 | 声称的角色 | 实际状态 |
|------|-----------|---------|
| BSR-MVP | Building State Runtime 最小原型 | 原型 + 6 个新架构层的试验场 |
| BSR-IFC | Building State Runtime for IFC（正式版） | 产品线主体：spec ×4 + core + Task Library |
| aads | Agent 状态协议层 | 与 BSR 平行的第二套状态概念 |
| paper_pipeline | 视觉重建 → IFC | BSR 的输入源（上游） |
| Digital-twin-platform | IIoT 数字孪生平台 | BSR 的呈现端/实时层（下游） |
| jackmen | 校园互助匹配 | 与 BSR 无关 |

**问题**：BSR-MVP 与 BSR-IFC 是同一个想法的两套实现，且各自在往前加新概念（MVP 加架构层，IFC 加 Task 库）。如果继续并行，将出现两个"BSR 真相"，spec 与代码的一致性（宪法第十六条）无法维持。

---

## 核心决策

### 决策 1：BSR-IFC 是唯一产品线

- 唯一的产品仓库：`BSR-IFC`。
- 唯一的状态真相：`BSR-IFC/spec/` 四份 spec + `core/` 运行时。
- 一切新概念必须先在 `spec/` 定稿，再进 `core/` 或 `tasks/`（宪法第十六条：Spec 先于代码）。

### 决策 2：BSR-MVP 降级为"原型验证场"

- BSR-MVP 不再作为独立产品演化，只承担**快速验证**职责：
  - 验证一个概念是否值得进入 BSR-IFC；
  - 验证一个算法的可行性（如 Surrogate、Optimizer）；
  - 跑 demo 给外部看。
- MVP 上出现的新概念，**不得在 MVP 继续堆代码**，而是以提案形式沉淀到 `BSR-IFC/spec/`（见 spec/05）。
- 判断标准：一个概念从 MVP 毕业进入 BSR-IFC，需要满足——

```
1. 有最小验证闭环（MVP 测试通过）
2. 有明确的 BSR-IFC 落点（spec 章节 / core 模块 / task 分类）
3. 不改变内核 API（kernel 0 修改原则）
```

### 决策 3：边界冻结——输入源与呈现端

| 仓库 | 冻结定位 | 对 BSR 的接口 |
|------|---------|--------------|
| paper_pipeline | BSR 的**输入源**：照片/点云 → IFC4 | 产出标准 IFC 文件，交给 BSR 导入 |
| Digital-twin-platform | BSR 的**呈现端**：实时状态 → 3D 大屏 | 消费 BSR 导出的状态/版本，不反向写 BSR |
| jackmen | 独立项目，与 BSR 叙事**解耦** | 无 |

这三个仓库不再参与 BSR 内核演化；其能力通过接口（IFC 文件 / 状态导出）与 BSR 连接。

### 决策 4：aads 是 BSR 的 Agent 基础设施

- aads 的 snapshot schema（Mission/Task/Tool 三层）作为 **BSR Agent 协议（spec/04）的实现基础**，负责"Agent 用 BSR 的过程本身可恢复"。
- 目标：任何 Agent 调用 BSR 的会话可 `track / resume / rollback`——与 BSR 对建筑数据的承诺一致。

---

## 收敛后的仓库全景

```
                  ┌─────────────────────────────────────┐
  输入源           │            BSR-IFC（唯一产品线）       │         呈现端
  paper_pipeline  │                                     │         Digital-twin-platform
  (照片→IFC)       │   User Goal                         │         (实时状态→3D)
        │         │     ↓ Goal Interpreter               │              ▲
        │  IFC    │     ↓ Task Planner ── Task Library    │              │ 状态导出
        │         │     ↓ Operation+Constraint+History    │              │
        └────────►│     ↓ IFC                            │──────────────┘
                  └─────────────────────────────────────┘
                        ▲
                        │ snapshot schema（Agent 会话可恢复）
                        │
                  aads（Agent 基础设施）
                  原型验证场：BSR-MVP（不再独立演化）
                  独立项目：jackmen（解耦）
```

---

## 迁移规则

任何新概念进入 BSR-IFC，按以下顺序：

```
1. 提案（spec/05 或新增 spec 章节，写明 Issue/Impact/Proposal）
2. 定稿（spec 冻结 → 编号）
3. 实现（core/ 或 tasks/，kernel 0 修改）
4. 验证（最小闭环：跑通 + 测试）
5. 同步（更新 README / docs，宪法 2.6）
```

禁止跳过 1 直接写代码。

---

## 收敛节奏（DoD）

- [ ] spec/00 本文件被接受
- [ ] spec/05 扩展层提案落定，MVP 新层不再直接加码
- [ ] spec/04 完成 aads 集成方案
- [ ] README 更新：BSR-IFC 声明为唯一产品线，其他仓库标注角色
- [ ] 下一次 MVP 新增概念时，先走迁移规则第 1 步

---

## 备注

本 spec 属于 Architecture 层（宪法层）：它定义四份业务 spec 的设计关系，不直接定义协议正文。若与 01-04 冲突，以 01-04 为准。

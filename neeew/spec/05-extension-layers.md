# BSR 扩展层提案 Spec v0.1

> **MVP 验证过的概念，正式进入 BSR-IFC 的提案。**
> 每个扩展层：MVP 里已验证什么、BSR-IFC 的落点在哪、成熟度如何、下一步是什么。

---

## 背景

BSR-MVP 在原型阶段验证了 6 个扩展架构层（Knowledge / Semantic / Digital Thread / Simulation / Memory / Governance）以及 2 个横切组件（Approval Gateway / Optimizer）。按 spec/00 决策 2，这些概念不再在 MVP 继续堆代码，而是以本提案形式沉淀，供 BSR-IFC 按迁移规则逐步吸收。

**统一原则**：所有扩展层必须满足 kernel 0 修改——它们包装、监听、扩展内核，不修改内核 API。

---

## 扩展层总览

| # | 层 | MVP 验证 | BSR-IFC 落点 | 成熟度 |
|---|-----|---------|-------------|--------|
| 1 | Knowledge 知识库 | ✅ GB 50016 条款 → Clause → Constraint → Evaluator 解耦 | spec/02 Layer 5 的正式化 + core/constraint 规则源 | 可吸收 |
| 2 | Semantic 语义对齐 | ✅ 视觉检测 → 工程实体（类型/材料/几何默认值） | core/ifc_extractor 的上游适配器（新 adapter） | 可吸收 |
| 3 | Digital Thread 数字线程 | ✅ 实体跨域身份：design/construction/cost/operation | spec/03 history 的扩展（实体生命周期视图） | 提案 |
| 4 | Simulation 仿真适配 | ✅ Fast Loop (Surrogate 毫秒) → Slow Loop (CAE 占位) | evaluator 体系的新评估来源（slow path） | 提案 |
| 5 | Memory 工程记忆 | ✅ 为什么改/谁批准/什么被拒 可查询 | spec/03 history 的扩展（rationale 字段 + 查询） | 可吸收 |
| 6 | Governance 治理审计 | ✅ 决策全链路可审计（Who/When/Why/Which） | core 新模块：governance.py（只记录，不改内核） | 可吸收 |

横切组件：

| 组件 | MVP 验证 | BSR-IFC 落点 | 成熟度 |
|------|---------|-------------|--------|
| Approval Gateway | ✅ LOW→COMMIT / MEDIUM→WAIT / HIGH→REJECT | spec/02 防护等级 L3/L4 的自动化策略 | 可吸收 |
| Optimizer | ✅ REJECT 后自动搜索可行方案（启发式） | Task 层工具（非内核），与 spec/04 Plan 层配合 | 提案 |

---

## 逐层提案

### 1. Knowledge Layer — 规范知识库

**MVP 验证**：`knowledge/knowledge_base.py` 实现 规范 → Clause → Constraint → Evaluator 解耦。规范变化只更新知识库，不修改 Evaluator 代码。

**BSR-IFC 落点**：
- spec/02 Layer 5（工程规则）目前是 JSON 配置，升级为"可编程 Clause"：
  - `Clause(standard, clause_id, description, condition_fn, severity)`——可复用的工程规则片段；
  - severity: `HARD`（拦截）/ `SOFT`（警告）/ `INFO`（记录）；
  - 评估输出带条款号（如 `GB 50016-2014 5.1.2`），可追溯到规范原文。
- core/constraint 增加 `knowledge.py`：注册表 + 求值器，内核不感知具体规则。

**验收标准**：新增一条规范条款只需在知识库加一个 Clause，不触碰 constraint/engine.py。

### 2. Semantic Layer — 视觉语义对齐

**MVP 验证**：`semantic/semantic_aligner.py` 把视觉检测结果（type/confidence/bbox/material_hint）提升为工程实体（工程类型推断 + 几何映射 + 材料映射 + 缺失属性默认值）。

**BSR-IFC 落点**：
- 作为 core/ifc_extractor 的**上游适配器**：`core/adapters/semantic_aligner.py`。
- 输入：paper_pipeline 的视觉输出（JSON）；输出：可直接导入的 BuildingState/IFC。
- 类型映射表（wall→Wall, column→Column…）与材料映射表（gypsum→Gypsum, aac_block→AAC…）作为配置，不硬编码进内核。

**验收标准**：paper_pipeline 输出 → semantic_aligner → BSR 导入链路可跑通（对照 MVP demo_phase6_8 Step 1）。

### 3. Digital Thread Layer — 数字线程

**MVP 验证**：`digital_thread/digital_thread.py` 实现实体生命周期身份映射——一个建筑对象在 Design（Revit/IFC ID）、Construction（P6 Task）、Cost（ERP SKU）、Operation（IoT Sensor）各域的身份，支持 register/get/link/traverse。

**BSR-IFC 落点**：
- spec/03 History 扩展：除 Change/Snapshot 外，增加**实体生命周期视图**——按 `element_id` 聚合其跨域身份与变更轨迹。
- core/history 增加 `thread.py`（只读扩展，不改 change.py 结构）。

**验收标准**：`bsr thread <element_id>` 输出该实体的跨域身份 + 变更历史。

### 4. Simulation Layer — 仿真适配

**MVP 验证**：`simulation_adapter/simulation_pipeline.py` 实现 Fast Loop（Surrogate，毫秒）→ Slow Loop（CAE，分钟~小时）分层：先快评估决定是否值得慢模拟，慢模拟结果回写知识库。

**BSR-IFC 落点**：
- evaluator 体系新增"slow path"评估来源：Proposal 先走 surrogate 快评，命中阈值再调度 CAE（EnergyPlus/OpenSees 占位）。
- 与 Knowledge Layer 联动：慢模拟结果沉淀为知识库经验数据。

**验收标准**：评估管线支持 快→慢 两段式，慢模拟为可插拔接口（当前占位）。

### 5. Memory Layer — 工程记忆

**MVP 验证**：`memory/project_memory.py` 保存为什么改（rationale）、谁批准（approver）、什么失败（failures）、什么方案被拒（rejected_proposals），支持语义查询（"为什么不用 Concrete？"→ 过去 Cost +18%, Schedule +20d, Rejected）。

**BSR-IFC 落点**：
- spec/03 History：Change 记录增加 `rationale` 字段（对齐 spec/00 决策 4 的 aads 集成）。
- core/history 增加查询接口：按目标/决策/方案反查历史理由。

**验收标准**：`bsr why <element_id> <option>` 返回历史决策理由。

### 6. Governance Layer — 治理审计

**MVP 验证**：`governance/governance.py` 的 `GovernanceRecord` 记录 Who/When/Why/Which Model/Which Rule/Which Version/approval，形成可审计决策链。

**BSR-IFC 落点**：
- core 新模块 `core/governance/`：记录每次 Operation 决策（含触发条款、评估结果、BSR commit id、审批方式），**只写不改**。
- spec/02 L3/L4 防护等级的人工确认动作统一进入治理记录。

**验收标准**：任意操作可回答"谁在什么时候、依据哪条规则、在哪个版本上做了什么决定"。

### 横切组件

**Approval Gateway**（`gateway/approval_gateway.py`）：风险分类策略 LOW→自动 COMMIT / MEDIUM→生成报告 WAIT_APPROVAL / HIGH→REJECT，作为 spec/02 防护等级的自动化策略层，包装 `kernel.propose()`，内核 0 修改。

**Optimizer**（`optimizer/optimizer.py`）：Proposal 被 REJECT 后自动生成候选（第一版厚度步长启发式，后续可换贝叶斯/遗传），多目标打分选最优。落点为 Task 层工具 + spec/04 Plan 层的自动重试策略。

---

## 迁移状态跟踪

| 层 | 状态 | 负责人 |
|----|------|--------|
| Knowledge | 提案（可吸收） | — |
| Semantic | 提案（可吸收） | — |
| Digital Thread | 提案 | — |
| Simulation | 提案 | — |
| Memory | 提案（可吸收） | — |
| Governance | 提案（可吸收） | — |
| Approval Gateway | 提案（可吸收） | — |
| Optimizer | 提案 | — |

状态流转：`提案 → 吸收中 → 已吸收 → 冻结`。本 spec 本身在冻结前可修订。

# BSR Agent Protocol Spec v0.1

> **Agent 如何与 BSR 通信。**
> 定义自然语言→操作的翻译协议。

---

## 待定

本 spec 在 BSR 运行时层完成后启用。当前阶段 BSR 提供 CLI + Python API，Agent 通过 cli 调用 BSR。

协议层的核心问题：
1. 自然语言指令如何解析为 Operation（意图识别）
2. 多步操作如何规划（Plan 层）
3. 约束检查未通过时如何反馈给 Agent 重试

这些问题在 spec 02 constraint 和 03 history 稳定后再定义。

---

## 当前通信模式（过渡方案）

```
Agent → bsr constrain --proto  path/to/file.ifc
Agent → bsr info path/to/file.ifc
Agent → Python: BSRExecutor.execute(operation)
```

所有约束检查结果以结构化 JSON 返回。

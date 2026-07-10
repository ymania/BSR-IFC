"""
BSR Protocol Handler — 自然语言 → Operation 的翻译器

层：Protocol（不是 Runtime，不依赖 LLM）

专门做过边界测试，覆盖 #ID、中文、英文属性名等场景。
"""

import re
from typing import Optional
from core.operation.executor import Operation


# 中文属性 → IFC 属性名映射
_PROP_MAP = {
    "高度": "Depth", "深度": "Depth", "长度": "Depth",
    "宽度": "Depth", "厚度": "Depth",
    "name": "Name", "名称": "Name", "名字": "Name",
}


def _resolve_id(text: str) -> str:
    text = text.strip()
    if text.startswith("#"):
        return text
    return text


class ProtocolHandler:
    PATTERNS = [
        # 改名: 把 XX 改名成/改名为 YY
        (r"(?:把|将)\s*(.+?)\s*(?:改名成|改名为)\s*(.+)",
         lambda m: Operation(
             name="ModifyProperty",
             params={"element_id": _resolve_id(m.group(1)), "property": "Name", "value": m.group(2)},
             protection_level=2, agent_prompt=m.group(0))),

        # 改名字/名称: 把 XX 的名字/名称改成 YY
        (r"(?:把|将)\s*(#?\S+)\s*(?:的名字|的名称|的name|的Name)\s*(?:改成|改为|设为)\s*(.+)",
         lambda m: Operation(
             name="ModifyProperty",
             params={"element_id": _resolve_id(m.group(1)), "property": "Name", "value": m.group(2)},
             protection_level=2, agent_prompt=m.group(0))),

        # 改任意属性: 把 XX 的 YY 改成 ZZ
        (r"(?:把|将)\s*(#?\S+)\s*的\s*(高度|深度|长度|宽度|厚度|Depth|depth|Name|name|名称|名字)\s*(?:改成|改为|设为|设置成)\s*([\d.]+)",
         lambda m: Operation(
             name="ModifyProperty",
             params={
                 "element_id": _resolve_id(m.group(1)),
                 "property": _PROP_MAP.get(m.group(2), m.group(2)),
                 "value": float(m.group(3)) if re.match(r'^[\d.]+$', m.group(3)) else m.group(3),
             },
             protection_level=2, agent_prompt=m.group(0))),

        # 改任意属性(字符串值): 把 XX 的 YY 改成 ZZ
        (r"(?:把|将)\s*(#?\S+)\s*的\s*(.+?)\s*(?:改成|改为|设为|设置成)\s*(.+)",
         lambda m: Operation(
             name="ModifyProperty",
             params={
                 "element_id": _resolve_id(m.group(1)),
                 "property": _PROP_MAP.get(m.group(2), m.group(2)),
                 "value": m.group(3),
             },
             protection_level=2, agent_prompt=m.group(0))),

        # 查: 查询/查看/检查/查一下/看看 XX
        (r"(?:查询|查看|检查|查一下|看看)\s*(#?\S+)",
         lambda m: Operation(
             name="SelectElement",
             params={"element_id": _resolve_id(m.group(1))},
             protection_level=1, agent_prompt=m.group(0))),

        # 删: 删除/移除/去掉 XX 因为 YY
        (r"(?:删除|移除|去掉)\s+(#?\S+?)(?:\s+因为\s+(.*))?$",
         lambda m: Operation(
             name="DeleteElement",
             params={
                 "element_id": _resolve_id(m.group(1)),
                 "reason": (m.group(2) or "未指定原因").strip(),
             },
             protection_level=4, agent_prompt=m.group(0))),

        # 删: 删除/移除/去掉 XX（无原因）
        (r"(?:删除|移除|去掉)\s+(#?\S+)",
         lambda m: Operation(
             name="DeleteElement",
             params={"element_id": _resolve_id(m.group(1)), "reason": "未指定原因"},
             protection_level=4, agent_prompt=m.group(0))),

        # 创建
        (r"(?:新建|创建|添加|增加)\s*(?:一个|个)?\s*(.+?)(?:\s*构件|\s*元素|\s*实体)?$",
         lambda m: Operation(
             name="CreateElement",
             params={"ifc_class": m.group(1)},
             protection_level=2, agent_prompt=m.group(0))),
    ]

    def parse(self, text: str) -> Optional[Operation]:
        text = text.strip()
        for pattern, builder in self.PATTERNS:
            m = re.search(pattern, text)
            if m:
                return builder(m)
        return None

    def parse_or_raise(self, text: str) -> Operation:
        op = self.parse(text)
        if op is None:
            raise ValueError(f"无法解析指令: {text}")
        return op

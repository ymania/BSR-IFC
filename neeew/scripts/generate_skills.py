#!/usr/bin/env python3
"""
BSR Task → Skill 生成器
========================
把 task-library/TaskNNN.md 批量转换为可安装的 Agent Skills（SKILL.md 格式）。

输出结构:
  skills/
  ├── manifest.json              # 所有 skill 的注册表（发现机制）
  ├── install.sh                 # 安装脚本（→ .claude/skills/ 或自定义目录）
  └── <slug>/
      └── SKILL.md               # 单个 skill（官方 Agent Skills 格式）

用法:
  python3 scripts/generate_skills.py            # 生成全部
  python3 scripts/generate_skills.py --check    # 校验 Task 字段完整性

规范依据: anthropics/skills 的 SKILL.md 格式（name + description frontmatter）
"""

import re
import json
import glob
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# task-library 位于仓库根目录；脚本可位于 neeew/scripts/ 或 scripts/，向上查找
_env_lib = os.environ.get("BSR_TASK_LIB", "").strip()
_TASK_LIB_CANDIDATES = [
    Path(_env_lib).resolve() if _env_lib else None,
    REPO_ROOT / "task-library",
    REPO_ROOT.parent / "task-library",
    REPO_ROOT.parent.parent / "task-library",
]
TASK_LIB = next((p for p in _TASK_LIB_CANDIDATES if p and p.is_dir()), REPO_ROOT / "task-library")
OUT_DIR = REPO_ROOT / "skills"
FIELD_ORDER = [
    "Goal", "Input", "Output", "Constraint",
    "Affected Classes", "Difficulty", "Frequency", "Business Value", "Source",
]


def parse_task(path: Path) -> dict:
    """解析单个 TaskNNN.md → 结构化 dict"""
    text = path.read_text(encoding="utf-8")
    task = {"file": path.name}

    # 标题: # Task001: rename-spaces
    m = re.search(r"^#\s*Task(\d+):\s*([\w-]+)", text, re.M)
    task["no"] = int(m.group(1)) if m else None
    task["slug"] = m.group(2) if m else path.stem
    task["id"] = f"Task{task['no']:03d}" if task["no"] else path.stem

    # 字段: **Goal**: ...
    for key in FIELD_ORDER:
        m = re.search(rf"^\*\*{re.escape(key)}\*\*:\s*(.+)$", text, re.M)
        task[key.lower().replace(" ", "_")] = m.group(1).strip() if m else ""

    # Description 段落（可选）
    m = re.search(r"^## Description\s*$", text, re.M)
    desc = text[m.end():].strip() if m else ""
    desc = re.sub(r"^\*|^\*", "", desc).strip()
    if desc and "Implementation in BSR tasks/" in desc:
        desc = ""
    task["description"] = desc

    return task


def build_skill_md(task: dict) -> str:
    """根据 Task 结构生成 SKILL.md（官方格式）"""
    slug = task["slug"]
    goal = task["goal"]
    inp = task["input"]
    out = task["output"]
    constraint = task["constraint"]
    classes = task["affected_classes"]
    difficulty = task["difficulty"]
    freq = task["frequency"]
    value = task["business_value"]
    source = task["source"]

    # description = 触发条件（何时该用这个 skill）
    desc = (
        f"BSR engineering task: {goal}. "
        f"Use when the user needs to {goal} in an IFC/BIM file. "
        f"Applicable when the model has {inp}."
    )

    lines = [
        "---",
        f"name: bsr-{slug}",
        f"description: |-",
        f"  {desc}",
        f"  TRIGGER — use whenever: the user mentions {goal}; the IFC contains {inp}; "
        f"or the user asks to fix/check/rename/report related to {classes}.",
        f"license: MIT",
        "---",
        "",
        f"# BSR Task — {slug}",
        "",
        f"> Task Library: `{task['id']}` · Difficulty {difficulty} · Frequency {freq} · Business Value {value}",
        "",
        "## When to use",
        "",
        f"- **Goal**: {goal}",
        f"- **Input**: {inp}",
        f"- **Trigger**: the user request maps to this engineering task; confirm with `bsr task --list` if unsure.",
        "",
        "## How to run",
        "",
        "```bash",
        f"bsr task {slug} <file.ifc>",
        "```",
        "",
        "### Parameters",
        "",
        "| Flag | Purpose |",
        "|------|---------|",
        "| `--proto` | PROTECTED mode (requires human confirmation) |",
        "",
        "### Pre-check (read-only, always safe)",
        "",
        "```bash",
        f"bsr inspect <file.ifc>      # 确认模型结构与 Affected Classes ({classes}) 是否存在",
        f"bsr check <file.ifc>        # 确认当前合规状态，作为 baseline",
        "```",
        "",
        "### Output contract",
        "",
        f"- **Output**: {out}",
        f"- **Constraint**: {constraint}",
        f"- **Affected Classes**: {classes}",
        "",
        "## Verification",
        "",
        "After running, verify:",
        "",
        "```bash",
        "bsr check <file.ifc>        # 无新增 FAIL",
        "bsr log <file.ifc>          # 修改已记录",
        "bsr diff <before.ifc> <file.ifc>  # 确认改动范围符合预期",
        "```",
        "",
        "## Notes",
        "",
        f"- Source: {source}",
        "- 本 skill 调用 BSR Runtime（Operation + Constraint + History），不直接触碰 IFC 文件。",
        "- 只做本任务描述的改动，不做 Delta 以外的操作（BSR 宪法第一条）。",
    ]
    return "\n".join(lines)


def build_manifest(tasks: list[dict]) -> dict:
    """生成 manifest.json（发现机制的核心）"""
    entries = []
    for t in tasks:
        entries.append({
            "id": t["id"],
            "slug": t["slug"],
            "skill_name": f"bsr-{t['slug']}",
            "path": f"skills/{t['slug']}/SKILL.md",
            "goal": t["goal"],
            "input": t["input"],
            "output": t["output"],
            "constraint": t["constraint"],
            "affected_classes": t["affected_classes"],
            "difficulty": t["difficulty"],
            "frequency": t["frequency"],
            "business_value": t["business_value"],
            "source": t["source"],
        })
    return {
        "schema_version": "1.0",
        "project": "BSR-IFC",
        "description": "BSR Task Library — 可安装的 Agent Skills 注册表",
        "total": len(entries),
        "install": {
            "claude_code": "ln -s $(pwd)/skills/<slug> ~/.claude/skills/bsr-<slug>  (或运行 install.sh)",
            "marketplace": "Claude Code: /plugin marketplace add ymania/BSR-IFC",
            "bsr_cli": "bsr skills install <slug>  (见 bsr skills 子命令)",
        },
        "skills": entries,
    }


def build_install_sh() -> str:
    """生成跨平台安装脚本（支持 Claude Code 标准目录 + 自定义）"""
    return r"""#!/usr/bin/env bash
# BSR Skills 安装脚本
#
# 用法:
#   ./skills/install.sh                 # 安装全部 skill 到 ~/.claude/skills/
#   ./skills/install.sh bsr-rename-spaces   # 安装单个
#   BSR_SKILLS_DIR=/path/to/dir ./skills/install.sh   # 自定义安装目录
#
# 目标目录（Claude Code 标准 skill 目录）:
#   ~/.claude/skills/    (Claude Code)
#   也可配合 plugin marketplace: /plugin marketplace add ymania/BSR-IFC

set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${BSR_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$TARGET"

install_one() {
    local name="$1"   # 形如 bsr-rename-spaces 或 rename-spaces 均可
    local slug="${name#bsr-}"
    local src="$SKILLS_DIR/$slug"
    if [[ ! -f "$src/SKILL.md" ]]; then
        echo "❌ 未找到 skill: $name (期望 $src/SKILL.md)" >&2
        exit 1
    fi
    ln -sfn "$src" "$TARGET/bsr-$slug"
    echo "✅ 已安装 bsr-$slug → $TARGET/bsr-$slug"
}

if [[ $# -eq 0 ]]; then
    for d in "$SKILLS_DIR"/*/; do
        [[ -f "$d/SKILL.md" ]] && install_one "$(basename "$d")"
    done
    echo "🎉 全部 BSR skills 已安装到 $TARGET (共 $(ls -d "$SKILLS_DIR"/*/ | wc -l | tr -d ' ') 个)"
else
    for slug in "$@"; do
        install_one "$slug"
    done
fi
"""


def domain_of(slug: str) -> str:
    """skill slug → 插件领域分组（marketplace 用）"""
    s = slug
    if any(k in s for k in ["fire", "medical-gas", "evacuation"]):
        return "fire-safety"
    if any(k in s for k in ["mep", "duct", "pipe", "system"]):
        return "mep"
    if any(k in s for k in ["bridge", "crane", "industrial"]):
        return "infrastructure"
    if any(k in s for k in ["wall", "slab", "beam", "column", "opening", "material"]):
        return "structure"
    if any(k in s for k in ["door", "window"]):
        return "openings"
    if any(k in s for k in ["space", "zone", "room", "storey", "hospital", "classroom", "school"]):
        return "space-planning"
    if any(k in s for k in ["property", "pset", "classification", "name", "rename",
                            "guid", "attribute", "owner", "value"]):
        return "property-data"
    if any(k in s for k in ["qto", "quantity", "export", "schedule", "stats",
                            "count", "report", "tree", "boundary"]):
        return "reporting"
    if any(k in s for k in ["validate", "syntax", "ifc2x3", "ids", "relationship",
                            "aggregate", "reverse", "containment", "abstract", "project"]):
        return "validation"
    return "general"


def build_marketplace(tasks: list[dict]) -> dict:
    """生成 .claude-plugin/marketplace.json（Claude Code 插件市场发现机制）"""
    groups = {}
    for t in tasks:
        groups.setdefault(domain_of(t["slug"]), []).append(f"./skills/{t['slug']}")
    return {
        "name": "bsr-task-skills",
        "owner": {"name": "ymania", "email": "3500249466@qq.com"},
        "metadata": {
            "description": "BSR Task Library — 50 个建筑 IFC 工程任务 skills（Agent Skills 格式）",
            "version": "1.0.0",
        },
        "plugins": [
            {"name": f"bsr-{grp}",
             "description": f"BSR {grp} skills ({len(paths)} 个)",
             "source": "./", "strict": False,
             "skills": paths}
            for grp, paths in sorted(groups.items())
        ],
    }


def main():
    check_only = "--check" in sys.argv
    files = sorted(glob.glob(str(TASK_LIB / "Task*.md")))

    tasks = []
    missing = {}
    for f in files:
        t = parse_task(Path(f))
        tasks.append(t)
        for k in ["goal", "input", "output", "constraint", "affected_classes",
                  "difficulty", "frequency", "business_value", "source"]:
            if not t.get(k):
                missing.setdefault(k, []).append(t["file"])

    print(f"解析 {len(tasks)} 个 Task")
    if missing:
        print("⚠️ 缺字段:")
        for k, v in missing.items():
            print(f"  {k}: {v}")
        if check_only:
            sys.exit(1)
    elif check_only:
        print("✅ 所有 Task 字段完整")
        return

    tasks.sort(key=lambda t: t["no"] or 0)

    # 写 skills/<slug>/SKILL.md
    written = 0
    for t in tasks:
        out = OUT_DIR / t["slug"] / "SKILL.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_skill_md(t), encoding="utf-8")
        written += 1

    # 写 manifest.json
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(build_manifest(tasks), ensure_ascii=False, indent=2),
        encoding="utf-8")

    # 写 install.sh
    (OUT_DIR / "install.sh").write_text(build_install_sh(), encoding="utf-8")
    os.chmod(OUT_DIR / "install.sh", 0o755)

    # 写 .claude-plugin/marketplace.json（插件市场发现）
    plugin_dir = REPO_ROOT / ".claude-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "marketplace.json").write_text(
        json.dumps(build_marketplace(tasks), ensure_ascii=False, indent=2),
        encoding="utf-8")

    print(f"✅ 生成 {written} 个 skills → {OUT_DIR}/")
    print(f"✅ manifest.json（注册表）")
    print(f"✅ install.sh（安装脚本）")
    print(f"✅ .claude-plugin/marketplace.json（Claude Code 插件市场）")


if __name__ == "__main__":
    main()

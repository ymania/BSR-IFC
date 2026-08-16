#!/usr/bin/env bash
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

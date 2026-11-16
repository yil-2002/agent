#!/usr/bin/env bash
# Dirijyor agentlari va qoidalarini loyiha repozitoriyasiga nusxalaydi.
# Bulut sessiyalari (claude.ai/code) plugin o'rnatmaydi, lekin repodagi
# .claude/agents/ va .claude/rules/ ni yuklaydi — shuning uchun shu nusxa kerak.
#
# Foydalanish:  scripts/install-to-repo.sh /yo'l/loyiha-repo
set -euo pipefail

src="$(cd "$(dirname "$0")/.." && pwd)"
dst="${1:?Foydalanish: $0 <loyiha-repo-papkasi>}"
[ -d "$dst" ] || { echo "Papka topilmadi: $dst" >&2; exit 1; }

mkdir -p "$dst/.claude/agents" "$dst/.claude/rules"
cp "$src"/agents/*.md "$dst/.claude/agents/"
cp "$src/rules/routing.md" "$dst/.claude/rules/dirijyor-routing.md"

echo "Nusxalandi:"
ls "$dst/.claude/agents" | sed 's/^/  .claude\/agents\//'
echo "  .claude/rules/dirijyor-routing.md"
echo "Endi o'sha repoda commit va push qiling."

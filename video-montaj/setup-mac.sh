#!/usr/bin/env bash
# AI-montaj ish papkasini Mac'da tayyorlaydi:
#   - Homebrew orqali ffmpeg, whisper-cpp, node o'rnatadi (bor bo'lsa o'tkazib yuboradi)
#   - Whisper modelini yuklaydi (nutqni matnga — subtitr uchun)
#   - ~/AI-montaj/{manbalar,namunalar,tayyor,ish} papkalarini yaratadi
#   - Claude uchun ish qoidalari (CLAUDE.md) ni papkaga qo'yadi
#
# Foydalanish:  video-montaj/setup-mac.sh [papka]   (standart: ~/AI-montaj)
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"
dst="${1:-$HOME/AI-montaj}"
model="${WHISPER_MODEL:-large-v3-turbo}"

[ "$(uname)" = "Darwin" ] || { echo "Bu skript macOS uchun." >&2; exit 1; }

if ! command -v brew >/dev/null; then
  echo "Homebrew topilmadi. Avval o'rnating: https://brew.sh" >&2
  exit 1
fi

for f in ffmpeg whisper-cpp node; do
  if brew list --formula "$f" >/dev/null 2>&1; then
    echo "✓ $f bor"
  else
    echo "→ $f o'rnatilmoqda..."
    brew install "$f"
  fi
done

mkdir -p "$dst"/{manbalar,namunalar,tayyor,ish,modellar}

mfile="$dst/modellar/ggml-$model.bin"
if [ -s "$mfile" ]; then
  echo "✓ Whisper modeli bor: $mfile"
else
  echo "→ Whisper modeli yuklanmoqda ($model, ~1.6 GB)..."
  curl -L --fail -o "$mfile.part" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$model.bin"
  mv "$mfile.part" "$mfile"
fi

if [ -e "$dst/CLAUDE.md" ] && ! cmp -s "$src/CLAUDE.md" "$dst/CLAUDE.md"; then
  cp "$dst/CLAUDE.md" "$dst/CLAUDE.md.bak"
  echo "! Eski CLAUDE.md → CLAUDE.md.bak"
fi
cp "$src/CLAUDE.md" "$dst/CLAUDE.md"

cat <<EOF

Tayyor: $dst
  manbalar/   — xom videolarni shu yerga tashlang
  namunalar/  — yoqqan uslubdagi video/rasm namunalari (ixtiyoriy)
  tayyor/     — Claude tayyor videoni shu yerga saqlaydi

Keyingi qadam: Claude ilovasi → Code → Local → Select folder → $dst
Keyin oddiy so'z bilan yozing, masalan:
  "manbalar/IMG_0804.MOV ni 60 soniyalik Reels qil: pauzalarni kes, so'zma-so'z subtitr, boshida katta sarlavha"
EOF

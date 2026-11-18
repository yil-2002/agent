# AI-montaj — ish qoidalari

Bu papka video montaj uchun. Foydalanuvchi oddiy so'z bilan nima kerakligini aytadi, sen montaj qilasan.
Foydalanuvchi bilan o'zbek tilida gaplash.

## Papkalar

| Papka | Vazifasi |
|---|---|
| `manbalar/` | Xom videolar. **Hech qachon o'zgartirma yoki o'chirma.** |
| `namunalar/` | Uslub namunalari (shrift, rang, subtitr ko'rinishi). Bor bo'lsa, avval ko'rib chiq. |
| `ish/` | Oraliq fayllar: transkript, kesilgan bo'laklar, Remotion loyihasi. |
| `tayyor/` | Yakuniy natija. Nom: `<manba-nomi>_v1.mp4`, keyingi tahrirlar `_v2`, `_v3`... |
| `modellar/` | Whisper modeli (`ggml-*.bin`). |

## Asboblar

- **FFmpeg** — kesish, birlashtirish, o'lcham (9:16, 1:1, 16:9), ovoz balandligi, sukutni topish, oddiy subtitr.
- **whisper-cpp** (`whisper-cli`) — nutqni matnga, so'z vaqtlari bilan.
- **Remotion** (Node) — motion grafika, animatsiyali so'zma-so'z subtitrlar, sarlavhalar, progress bar.

## Ish tartibi

1. **Ko'rib chiq.** `ffprobe` bilan davomiylik, o'lcham, fps, aylantirish (rotation) ni aniqla.
   Kerak bo'lsa bir nechta kadrni `ffmpeg -vf fps=1/3` bilan chiqarib, ko'z bilan ko'r.
2. **Transkript.** Avval ovozni 16 kHz mono WAV ga o'tkaz, keyin:
   ```bash
   ffmpeg -y -i manbalar/X.MOV -ar 16000 -ac 1 ish/X.wav
   whisper-cli -m modellar/ggml-large-v3-turbo.bin -f ish/X.wav -l auto -ojf -osrt -of ish/X
   ```
   `-ojf` so'z darajasidagi vaqtlarni beradi (`ish/X.json`). Til aniq bo'lsa `-l uz` / `-l ru` qo'y.
3. **Reja.** Nimani kesish, qayerga nima qo'yishni qisqa ro'yxat qilib foydalanuvchiga ko'rsat.
   Vazifa aniq bo'lsa, so'ramasdan bajaraver.
4. **Kesish.** Pauzalar: `silencedetect=noise=-35dB:d=0.4`, keyin `trim`/`atrim` + `concat`.
   Takroriy yoki xato gaplarni transkriptdan top.
5. **Grafika va subtitr.**
   - Oddiy subtitr: `ffmpeg -vf subtitles=ish/X.srt` (libass kerak; ishlamasa Remotion'ga o't).
   - Chiroyli/animatsiyali subtitr, sarlavha, motion grafika: Remotion.
     Loyiha yo'q bo'lsa `ish/remotion/` da yarat (`npx create-video@latest`), so'z vaqtlarini
     JSON dan o'qib, `@remotion/captions` bilan ko'rsat. Render: `npx remotion render`.
6. **Eksport.** H.264 + AAC, `-movflags +faststart`, `-crf 18`. Reels/Shorts uchun 1080×1920, 30 fps.
7. **Tekshir.** Natijadan bir nechta kadr chiqarib ko'r: subtitr kesilmaganmi, yuz yopilmaganmi,
   ovoz-video sinxronmi. Keyin `tayyor/` dagi fayl yo'lini ayt.

## Qoidalar

- Manba fayllarni o'zgartirma; har doim yangi fayl yoz.
- Subtitr ekranning pastki uchdan birida, yuzni yopmasin; xavfsiz zona — chetlardan 8%.
- Uzun render oldidan 5–10 soniyalik qisqa sinov render qil.
- Bir buyruq 10 daqiqadan uzoq ishlasa, foydalanuvchiga taxminiy vaqtni ayt.

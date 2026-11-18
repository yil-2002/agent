# 🎬 AI-montaj — Claude bilan Mac'da video montaj

Video tashlaysiz, nima kerakligini so'z bilan yozasiz — Claude o'zi kesadi, subtitr va motion grafika qo'shadi.
Ichida: **FFmpeg** (montaj), **Whisper** (nutq → subtitr), **Remotion** (motion grafika).

## 1. O'rnatish (bir marta)

Kerak: [Homebrew](https://brew.sh) va [Claude desktop ilovasi](https://claude.ai/download).

```bash
git clone https://github.com/yil-2002/agent
agent/video-montaj/setup-mac.sh
```

Skript `ffmpeg`, `whisper-cpp`, `node` ni o'rnatadi, Whisper modelini (~1.6 GB) yuklaydi va
`~/AI-montaj` papkasini yaratadi:

```
~/AI-montaj/
  manbalar/    ← xom videolar
  namunalar/   ← uslub namunalari (ixtiyoriy)
  tayyor/      ← tayyor videolar
  ish/         ← oraliq fayllar
  CLAUDE.md    ← Claude uchun montaj qoidalari
```

Boshqa papka: `setup-mac.sh ~/Desktop/Montaj`. Kichikroq model: `WHISPER_MODEL=small setup-mac.sh`.

## 2. Ishlatish

1. Videoni `~/AI-montaj/manbalar/` ga tashlang.
2. Claude ilovasi → **Code** → **New session** → **Local** → **Select folder** → `AI-montaj`.
3. Oddiy so'z bilan yozing:

> manbalar/IMG_0804.MOV dan 60 soniyalik Reels qil: pauzalarni kes, so'zma-so'z sariq subtitr,
> boshida "60 soniya" degan katta sarlavha, oxirida obuna bo'lish chaqirig'i.

Tayyor video `tayyor/` papkasida paydo bo'ladi. Tuzatish kerak bo'lsa, shu sessiyada yozing ("subtitrni kattaroq qil").

## Maslahatlar

- Model sifatida Opus tanlang — montaj ko'p qadamli ish.
- `namunalar/` ga yoqqan videongizdan skrinshot qo'ysangiz, Claude uslubni shunga moslaydi.
- Ish qoidalarini o'zgartirish uchun `~/AI-montaj/CLAUDE.md` ni tahrirlang.

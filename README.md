# 🎼 Dirijyor — Claude Code uchun multi-agent plugin

Asosiy model (Opus) dirijyor bo'lib ishlaydi: har bir vazifani qiyinlik darajasiga qarab ajratadi va mos modelga yo'naltiradi. Maqsad: Claude limitlaridan unumli foydalanish, sifatni yo'qotmasdan.

```
                    ┌──────────────────────┐
     Foydalanuvchi ─▶│  Opus (dirijyor)     │◀─ yakuniy tekshiruv
                    └──────────┬───────────┘
          ┌────────────────────┼─────────────────────┐
          ▼                    ▼                     ▼
  ┌───────────────┐   ┌────────────────┐   ┌──────────────────────┐
  │ builder       │   │ scout          │   │ bulk-worker          │
  │ Sonnet        │   │ Haiku          │   │ → DeepSeek Flash     │
  │ o'rta ishlar  │   │ qidiruv, oson  │   │ ommaviy / mexanik    │
  └───────────────┘   └────────────────┘   └──────────────────────┘
```

| Daraja | Ijrochi | Qanday vazifalar |
|---|---|---|
| **S — qiyin** | Opus (o'zi) | Arxitektura, murakkab mantiq, nozik bug'lar, xavfsizlik, yakuniy review |
| **A — o'rta** | `dirijyor:builder` (Sonnet) | Aniq spetsifikatsiya bo'yicha feature, o'rta bug'lar |
| **B — oson** | `dirijyor:scout` (Haiku) | Qidiruv, o'qish, xulosa, log tahlili |
| **C — ommaviy** | `dirijyor:bulk-worker` (DeepSeek) | Ko'p fayldagi takroriy ish, boilerplate, testlar, tarjima |

To'liq qoidalar: [`rules/routing.md`](rules/routing.md).

## Ichida nima bor

```
.claude-plugin/
  plugin.json        # plugin metama'lumoti
  marketplace.json   # shu repo o'zi marketplace — o'rnatish uchun
agents/              # scout (Haiku), builder (Sonnet), bulk-worker (Haiku → DeepSeek)
hooks/hooks.json     # SessionStart: har sessiya boshida routing qoidalarini kontekstga qo'shadi
rules/routing.md     # routing qoidalari matni
scripts/install-to-repo.sh  # agentlar + qoidalarni loyiha repoga nusxalash (bulut uchun)
```

Plugin ichidagi `CLAUDE.md` Claude Code tomonidan yuklanmaydi, shuning uchun qoidalar `SessionStart` hook orqali kiritiladi.

## O'rnatish

### O'z kompyuteringizda (barcha loyihalar uchun)

```bash
claude plugin marketplace add yil-2002/agent
claude plugin install dirijyor@dirijyor
```

Asosiy modelni Opus qilish uchun `~/.claude/settings.json` ga qo'shing (plugin bu sozlamani o'zgartira olmaydi):

```json
{ "model": "opus" }
```

Tekshirish: Claude Code ichida `/agents` buyrug'i `dirijyor:scout`, `dirijyor:builder`, `dirijyor:bulk-worker` agentlarini ko'rsatishi kerak.

### Bulut sessiyalarida (claude.ai/code, telefon ilovasi)

Bulut sessiyasi plugin **o'rnatmaydi** — hatto repodagi `.claude/settings.json` da `enabledPlugins` bo'lsa ham.
U faqat repoga commit qilingan `.claude/agents/` va `.claude/rules/` ni yuklaydi. Shuning uchun agentlar va
qoidalarni loyiha repozitoriyasiga nusxalang:

```bash
git clone https://github.com/yil-2002/agent
agent/scripts/install-to-repo.sh /yo'l/loyiha-repo
cd /yo'l/loyiha-repo && git add .claude && git commit -m "Add dirijyor agents" && git push
```

Natija: `.claude/agents/{scout,builder,bulk-worker}.md` va `.claude/rules/dirijyor-routing.md`.
Bunday repoda agentlar `scout`, `builder`, `bulk-worker` nomi bilan ko'rinadi. Qoidalar yangilansa, skriptni qayta ishga tushiring.

Asosiy modelni Opus qilish uchun o'sha reponing `.claude/settings.json` iga `{"model": "opus"}` qo'shing.

> O'z kompyuteringizda plugin o'rnatilgan bo'lsa, nusxalangan repoda agentlar ikki marta ko'rinadi
> (`scout` va `dirijyor:scout`) — bu zararsiz, repodagi nusxa ishlatiladi.

Loyihaga xos ma'lumotlarni (fayl xaritasi, tekshirish buyruqlari) loyihaning o'z `CLAUDE.md` fayliga yozing.

### DeepSeek (ixtiyoriy, C-daraja uchun)

`bulk-worker` [PsChina/deepseek-as-subagent](https://github.com/PsChina/deepseek-as-subagent) MCP serveridan foydalanadi:

```bash
git clone https://github.com/PsChina/deepseek-as-subagent
cd deepseek-as-subagent
./install.sh          # avval install.sh ni ko'rib chiqing
```

Kalit `~/.deepseek-mcp/config.json` ga yoziladi (Windows'da `DEEPSEEK_API_KEY`). DeepSeek ulanmagan bo'lsa, C-daraja ishlar avtomatik `builder` ga o'tadi.

> ⚠️ DeepSeek coding rejimida Bash'ni sizning kompyuteringizda ishga tushiradi (OS sandbox emas). Unga maxfiy ma'lumot yubormang.

Bulut sessiyasida DeepSeek uchun qo'shimcha sozlash kerak: muhit tarmog'ida `api.deepseek.com` ga ruxsat va kalitni muhitning network secret'ida saqlash.

## 🎬 Video montaj (Mac)

Claude bilan video montaj qilish uchun tayyor ish papkasi (FFmpeg + Whisper + Remotion): [`video-montaj/`](video-montaj/README.md).

## Yangilash

```bash
claude plugin marketplace update dirijyor
```

`plugin.json` dagi `version` o'zgartirilganda foydalanuvchilar yangi versiyani oladi.

## Tekshirish

Subagentlar haqiqatda to'g'ri modelda ishlayotganini ko'rish:

```bash
grep -rhoE '"model":"[^"]+"' ~/.claude/projects/*/*/subagents/ 2>/dev/null | sort | uniq -c
```

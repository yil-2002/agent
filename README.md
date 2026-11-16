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

### Bulut sessiyalarida (claude.ai/code) va jamoa uchun

Loyiha repozitoriyasidagi `.claude/settings.json` ga qo'shing — repo ochilganda plugin avtomatik taklif qilinadi va yoqiladi:

```json
{
  "model": "opus",
  "extraKnownMarketplaces": {
    "dirijyor": { "source": { "source": "github", "repo": "yil-2002/agent" } }
  },
  "enabledPlugins": { "dirijyor@dirijyor": true }
}
```

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

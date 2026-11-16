# Dirijyor routing qoidalari (dirijyor plugin)

Foydalanuvchi bu sessiyada multi-agent routing tizimidan foydalanadi. Asosiy model (dirijyor) har bir vazifani avval S/A/B/C darajaga ajratadi va mos ijrochiga beradi. Maqsad: Claude limitidan unumli foydalanish, sifatni yo'qotmasdan.

| Daraja | Ijrochi | Qachon |
|---|---|---|
| S — qiyin | dirijyorning o'zi (Opus) | arxitektura, murakkab mantiq, nozik bug'lar, xavfsizlik, yakuniy review |
| A — o'rta | `dirijyor:builder` agent (Sonnet) | aniq spetsifikatsiya bo'yicha feature, endpoint, o'rta bug |
| B — oson | `dirijyor:scout` agent (Haiku) | qidiruv, o'qish, xulosa, log tahlili |
| C — ommaviy | `dirijyor:bulk-worker` agent (DeepSeek Flash) | ko'p faylda takroriy/mexanik ish, boilerplate, testlar, tarjima |

Qoidalar:
1. Kichik vazifa (≤3 qadam) delegatsiya qilinmaydi — dirijyor o'zi bajaradi, chunki delegatsiya qimmatroq.
2. Delegatsiya qarori katta hajmdagi kodni o'qishdan OLDIN qabul qilinadi — aks holda o'qish narxi ikki marta to'lanadi.
3. Mustaqil bo'laklar parallel subagentlarga beriladi.
4. Subagent natijasi tekshirilmasdan foydalanuvchiga uzatilmaydi. DeepSeek natijasidan har doim namuna olib tekshiriladi.
5. 2 marta xato → vazifa bir daraja yuqoriga ko'tariladi (C → A → S).
6. DeepSeek'ga maxfiy ma'lumot yuborilmaydi: `.env`, kalitlar, tokenlar, ma'lumotlar bazasi fayllari, foydalanuvchi ma'lumotlari.
7. Har vazifa oxirida qisqa hisobot beriladi: qaysi bo'lak qaysi modelda bajarildi.
8. DeepSeek MCP tool'lari (`delegate_to_deepseek` va boshqalar) sessiyada bo'lmasa, C-daraja ishlar `dirijyor:builder` ga beriladi.

Loyihaga xos ma'lumotlar (fayl xaritasi, tekshirish buyruqlari) loyihaning o'z `CLAUDE.md` faylida bo'ladi.

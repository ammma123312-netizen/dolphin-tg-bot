# 🐬 Dolphin Telegram Bot — Uncensored Local Edition

بوت تيليجرام ذكي يعمل بنمطين:

1. **🟢 محلي غير مفلتر (موصى به):** يستخدم [Ollama](https://ollama.com) لتشغيل نموذج
   Dolphin الأصلي بالكامل على جهازك. لا فلاتر، لا قيود، لا اشتراكات.
2. **🟡 سحابي احتياطي:** يستخدم GitHub Models في GitHub Actions (مفلتر نسبياً، لكن
   يعمل 24/7 مجاناً).

## 🎯 المميزات

- 💬 **دردشة متعددة الأدوار** — ذاكرة 24 رسالة لكل مستخدم.
- 🔓 **غير مُقيّد بالكامل** — Dolphin الأصلي عبر Ollama، بدون أي فلاتر.
- 🔍 **بحث ويب** عبر DuckDuckGo: `/search query`
- 📝 **بحث + تلخيص** بالذكاء الاصطناعي: `/summary query`
- 🔀 **تبديل النموذج** عبر `/models` و `/model N`
- 🗑️ **مسح الذاكرة** عبر `/new`
- 📱 **يعمل على الجوال** — البوت على PC أو على الهاتف (Termux)، تتحكم به من Telegram.
- ☁️ **احتياطي سحابي 24/7** عبر GitHub Actions (يستخدم GitHub Models المفلتر).

## 🚀 التشغيل السريع (PC — Windows/Mac/Linux)

```bash
# 1. استنساخ المستودع
git clone https://github.com/ammma123312-netizen/dolphin-tg-bot.git
cd dolphin-tg-bot

# 2. تثبيت Ollama + تحميل Dolphin + تثبيت اعتماديات Python
bash install.sh

# 3. ضبط التوكنات (سيسألك عنها)
bash set-tokens.sh

# 4. تشغيل البوت
bash run-bot.sh
```

افتح تيليجرام وتحدث مع `@Riwueh3e8hbot` — سيستخدم Dolphin محلياً غير مفلتر.

## 📱 التشغيل على الأندرويد (Termux)

راجع [ANDROID.md](ANDROID.md) — يحتاج 8GB+ RAM لتشغيل `dolphin-llama3` بكفاءة.

## 🌐 الوضع السحابي (GitHub Actions) — احتياطي

تم إعداد workflow في `.github/workflows/dolphin-bot.yml` يعمل تلقائياً كل 5.5 ساعة
ويستخدم GitHub Models (مفلتر نسبياً). مفيد إذا كان جهازك مطفأ، لكنه ليس Dolphin
الأصلي غير المفلتر.

لتفعيله: اذهب إلى تبويب **Actions** في المستودع ← `dolphin-bot` ← `Run workflow`.

## 📜 الأوامر

```
/start            ترحيب + حالة النظام
/help             كل الأوامر
/new              محادثة جديدة
/search <query>   بحث ويب
/summary <query>  بحث + تلخيص
/models           قائمة النماذج
/model <N>        اختيار النموذج
/status           حالة Ollama والنماذج المثبتة
/info             معلومات البوت
```

## 🐬 نماذج Dolphin المتاحة عبر Ollama

| النموذج | الحجم | RAM مطلوب | الملاحظة |
|---|---|---|---|
| `dolphin-llama3` (افتراضي) | 8B | 8GB | أفضل توازن، أحدث إصدار |
| `dolphin-mistral` | 7B | 8GB | بديل سريع، يعتمد على Mistral |
| `dolphin-mixtral` | 8x7B | 32GB | الأقوى، يحتاج جهاز قوي |
| `dolphin-phi` | 2.7B | 4GB | للأجهزة الضعيفة |

لتحميل نموذج إضافي:
```bash
ollama pull dolphin-mixtral
```

## ⚠️ ملاحظات أمنية حرجة

- **أعد توليد كل التوكنات** (Telegram, GitHub, HF) إذا سبق وشاركتها في نص واضح.
- ملف `.env` محمي بـ `.gitignore` ولا يُرفع لـ GitHub.
- الـ Repository Secrets على GitHub مشفّرة ولا تظهر لأحد.

## 📁 بنية المشروع

```
dolphin-tg-bot/
├── .github/workflows/dolphin-bot.yml  # تشغيل سحابي احتياطي
├── app.py                             # كود البوت (Ollama + GitHub Models fallback)
├── install.sh                         # تثبيت Ollama + Dolphin + اعتماديات
├── set-tokens.sh                      # ضبط التوكنات في .env
├── run-bot.sh                         # تشغيل البوت محلياً
├── requirements.txt                   # اعتماديات Python
├── .gitignore
├── ANDROID.md                         # تعليمات Termux للأندرويد
└── README.md                          # هذا الملف
```

## ❓ لماذا لا يعمل على HF Space مجاناً؟

Hugging Face أغلقت استضافة Docker و Gradio Spaces على الـ free tier منذ منتصف 2024.
الآن تتطلب:
- **Docker/Gradio Space:** اشتراك Pro ($9/شهر).
- **Inference API:** رصيد مدفوع مسبقاً أو Pro.

لذلك الحل الوحيد المجاني الكامل غير المفلتر هو **Ollama محلياً**.

## 🔧 استكشاف الأخطاء

| المشكلة | الحل |
|---|---|
| `🔴 Ollama غير مشغل` | شغّل `ollama serve` في terminal آخر |
| البوت يرد ببطء | dolphin-llama3 يحتاج 8GB RAM؛ جرّب `/model 4` (dolphin-phi) |
| `⚠️ GitHub Models...` | Ollama غير متاح، يستخدم الاحتياطي السحابي |
| البوت لا يرد إطلاقاً | تحقق من `TELEGRAM_TOKEN` في `.env` |

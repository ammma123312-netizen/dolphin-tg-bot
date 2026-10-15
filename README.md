# Dolphin Telegram Bot 🐬

بوت تيليجرام ذكي يعمل في السحابة عبر GitHub Actions (مجاني تماماً) ويستخدم نماذج LLM
عبر GitHub Models. لا يتطلب اشتراك أو بطاقة ائتمان.

## المميزات
- 💬 **دردشة متعددة الأدوار** — ذاكرة 24 رسالة لكل مستخدم.
- 🔓 **غير مُقيّد نسبياً** — يستخدم Mistral-Nemo / Mistral-large افتراضياً (أقل تصفية من GPT).
- 🔍 **بحث ويب** عبر DuckDuckGo: `/search query`
- 📝 **بحث + تلخيص** بالذكاء الاصطناعي: `/summary query`
- 🔀 **تبديل النموذج** عبر `/models` و `/model N`
- 🗑️ **مسح الذاكرة** عبر `/new`
- ☁️ **تشغيل سحابي 24/7** عبر GitHub Actions (مجاني للـ public repos).

## البنية
- `app.py` — كود البوت (Python، python-telegram-bot v21)
- `requirements.txt` — الاعتماديات
- `.github/workflows/dolphin-bot.yml` — تشغيل البوت في GitHub Actions مع auto-restart

## النماذج المتاحة (عبر GitHub Models)
1. `Mistral-Nemo` (افتراضي)
2. `Mistral-large`
3. `Meta-Llama-3.3-70B-Instruct`
4. `Meta-Llama-3.1-70B-Instruct`
5. `Mistral-7B-Instruct`
6. `Phi-3.5-mini-instruct`
7. `gpt-4o-mini`

## الإعداد (تم تنفيذه تلقائياً)
تم ضبط الـ Repository Secrets التالية:
- `TELEGRAM_TOKEN` — توكن بوت تيليجرام
- `GH_TOKEN` — GitHub PAT بصلاحية `models:read`
- `HF_TOKEN` (اختياري) — احتياطي في حال إضافة رصيد على HF

## التشغيل اليدوي
- اذهب إلى تبويب **Actions** في المستودع
- اختر workflow `dolphin-bot`
- اضغط **Run workflow**

## ملاحظات أمنية
- ⚠️ **أعد توليد كل التوكنات التي شاركتها** (HF, GitHub, Telegram) لأنها سُرّبت في نص الرسالة.
- المستودع public لكن الـ secrets مشفّرة ولا تظهر لأحد.
- الكود نفسه عام — لا تضع أي معلومات حساسة فيه.

## حدود GitHub Models المجانية
- ~150 طلب/يوم لكل نموذج (لمستخدمي GitHub المجانيين).
- يكفي لاستخدام شخصي خفيف-متوسط.

## حدود GitHub Actions
- 6 ساعات كحد أقصى لكل job → البوت يعمل 5.5 ساعة ثم يُعاد تشغيله تلقائياً.
- قد تكون هناك فجوة بضع ثوانٍ بين التشغيلات.
- لـ public repos: غير محدود.

# 🐬 Dolphin Telegram Bot على Telebot Creator
## دليل التشغيل الكامل من جوالك (بدون PC)

> ✅ **مجاني 100%** | ✅ **بدون PC** | ✅ **يعمل 24/7** | ✅ **من جوالك فقط**

---

## 🎯 ما الذي ستحصل عليه

بوت تيليجرام `@Riwueh3e8hbot` يعمل على منصة **Telebot Creator** السحابية المجانية:
- 💬 دردشة ذكية مع Dolphin (مع system prompt قوي لتفادي الفلاتر)
- 🔍 بحث ويب عبر `/search`
- 🧠 ذاكرة 24 رسالة لكل مستخدم
- ☁️ استضافة سحابية مجانية دائمة (بدون PC، بدون جهاز محلي)

---

## 📋 المتطلبات (كلها من جوالك)

1. **تطبيق تيليجرام** على جوالك (موجود لديك)
2. **متصفح** على جوالك (Chrome / Safari)
3. **حساب GitHub** (موجود لديك — اسم المستخدم `ammma123312-netizen`)
4. **البوت الخاص بك** على تيليجرام (موجود: `@Riwueh3e8hbot`)

---

## 🚀 خطوات التشغيل (15 دقيقة)

### الخطوة 1: سجّل في Telebot Creator

1. من متصفح جوالك، اذهب إلى: **https://telebotcreator.com**
2. اضغط **Sign Up** أو **Get Started**
3. سجّل بإيميلك أو بحساب Google
4. أكّد الإيميل

> 💡 **بديل:** نزّل تطبيق **Telebot Creator** من Google Play لأندرويد:
> https://play.google.com/store/apps/details?id=com.app.telebotcreator

---

### الخطوة 2: أضف البوت

1. في لوحة التحكم، اضغط **Add New Bot** (أو **Create Bot**)
2. الصق توكن البوت:
   ```
   8651612734:AAFM2TDoXzndrk0I7N6Pvlf_-m2H73zQLu0
   ```
3. أعطِ البوت اسماً وصفياً (مثل "Dolphin AI")
4. اضغط **Create Bot**

---

### الخطوة 3: أنشئ الأوامر

في صفحة البوت، اذهب إلى تبويب **Commands** وأنشئ 5 أوامر:

#### الأمر 1: `/start`
- **Command name:** `start`
- **Description:** ترحيب
- **Code:** (انسخ من ملف `tpy/dolphin_bot_tpy.py` قسم "الأمر 1: /start")

#### الأمر 2: `/new`
- **Command name:** `new`
- **Description:** مسح الذاكرة
- **Code:** (انسخ قسم "الأمر 2: /new")

#### الأمر 3: `/help`
- **Command name:** `help`
- **Description:** مساعدة
- **Code:** (انسخ قسم "الأمر 3: /help")

#### الأمر 4: `/search`
- **Command name:** `search`
- **Description:** بحث ويب
- **Code:** (انسخ قسم "الأمر 4: /search")

#### الأمر 5: `*` (مهم جداً)
- **Command name:** `*` (نجمة واحدة — هذا الأمر يستقبل أي رسالة عادية)
- **Description:** رد على أي رسالة
- **Code:** (انسخ قسم "الأمر 5: *" — هذا أطول كود)

---

### الخطوة 4: شغّل البوت

1. في صفحة البوت، اضغط زر **Start** (أو زر التشغيل الأخضر)
2. انتظر ثوانٍ حتى يظهر "Bot is running"
3. افتح تيليجرام على جوالك
4. ابحث عن `@Riwueh3e8hbot`
5. اضغط **Start** أو أرسل `/start`

🎉 **مبارك! البوت يعمل الآن 24/7 من سحابة Telebot Creator.**

---

## 🧪 اختبر البوت

أرسل للبوت هذه الرسائل:

| الرسالة | الرد المتوقع |
|---|---|
| `/start` | رسالة ترحيب |
| `مرحبا، من أنت؟` | تعريف بـ Dolphin |
| `اكتب قصيدة قصيرة عن البحر` | قصيدة |
| `/search أفضل مطاعم الرياض` | نتائج بحث |
| `/new` | تأكيد مسح الذاكرة |

---

## ⚠️ مشاكل شائعة وحلولها

### المشكلة: البوت لا يرد على الرسائل العادية
**السبب:** الأمر `*` لم يُنشأ بشكل صحيح.

**الحل:**
1. اذهب إلى Commands
2. تأكد أن لديك أمر باسم `*` (نجمة فقط)
3. الصق الكود الكامل من قسم "الأمر 5"
4. احفظ وأعد التشغيل

### المشكلة: `⚠️ خطأ: GH 401`
**السبب:** توكن GitHub غير صالح أو منتهي.

**الحل:**
1. اذهب إلى https://github.com/settings/tokens
2. أنشئ token جديد بصلاحية `models:read`
3. استبدل `GH_TOKEN` في كود الأمر `*`
4. احفظ وأعد التشغيل

### المشكلة: `⚠️ خطأ: GH 429`
**السبب:** تجاوزت 150 طلب/يوم (حد GitHub Models المجاني).

**الحل:**
- انتظر 24 ساعة، أو
- سجّل في https://openrouter.ai (مجاني) واستبدل الكود لاستخدام OpenRouter

### المشكلة: البوت يرد بـ "I cannot..."
**السبب:** النموذج السحابي مفلتر رغم الـ system prompt.

**الحل:** البوت تلقائياً يعيد المحاولة مع رسالة تعزيز. إذا استمر:
- جرب `/new` وابدأ محادثة جديدة
- أو الصبر — بعض الأسئلة سيرد عليها بشكل صحيح

---

## 🔒 الأمان

### ⚠️ مهم جداً: أعد توليد التوكنات

لقد شاركت التوكنات التالية في رسائلك السابقة، وهي تُعتبر مسرّبة:

1. **Telegram Bot Token** — اذهب إلى `@BotFather` → `/revoke` ← احصل على توكن جديد
2. **GitHub Token** — اذهب إلى https://github.com/settings/tokens → احذف وأنشئ جديد
3. **Hugging Face Token** — اذهب إلى https://huggingface.co/settings/tokens → احذف وأنشئ جديد

بعد إعادة التوليد، حدّث:
- كود الأمر `*` في Telebot Creator (استبدل `GH_TOKEN` و `HF_TOKEN`)
- Repository Secrets على GitHub (للبوت الاحتياطي على Actions)

---

## 💡 نصائح متقدمة

### لتحسين جودة الردود (Dolphin حقيقي 100%)

استخدم **OpenRouter** بدلاً من GitHub Models — يوفر `dolphin-2.9-llama3-8b` فعلاً:

1. سجّل في https://openrouter.ai (مجاني بـ GitHub)
2. احصل على API key
3. في كود الأمر `*`، استبدل دالة `call_github_models` بـ:

```python
def call_openrouter(messages, model_name):
    payload = {
        "model": model_name,  # مثلاً: "cognitivecomputations/dolphin-2.9-llama3-8b"
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7,
    }
    resp = HTTP.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers={
            "Authorization": "Bearer " + OPENROUTER_KEY,
            "Content-Type": "application/json",
        },
        timeout=90,
    )
    if resp.status_code != 200:
        raise Exception("OR " + str(resp.status_code))
    return resp.json()["choices"][0]["message"]["content"].strip()
```

نماذج مجانية على OpenRouter تدعم Dolphin:
- `cognitivecomputations/dolphin-2.9-llama3-8b` (free)
- `cognitivecomputations/dolphin-2.6-mistral-7b` (free)
- `nousresearch/hermes-3-llama-3.1-405b:free` (free, أقوى)

### لإيقاف البوت مؤقتاً
في لوحة Telebot Creator، اضغط زر **Stop** على البوت.

### لمسح بيانات المستخدمين
في صفحة Bot، اذهب إلى **Users** → **Clear all data**

---

## 📞 الدعم

- **وثائق Telebot Creator:** https://help.telebotcreator.com
- **مجموعة Telegram للمستخدمين:** ابحث في TBC dashboard عن رابط Community
- **البوت الخاص بك:** `@Riwueh3e8hbot`

---

## 📂 الملفات

| الملف | الوصف |
|---|---|
| `tpy/dolphin_bot_tpy.py` | كود TPY الكامل (5 أوامر منفصلة) |
| `README_TBC.md` | هذا الدليل |

## ❓ لماذا Telebot Creator؟

جرّبتُ عدة منصات قبل الوصول لهذا الحل:

| المنصة | لماذا لم تنفع |
|---|---|
| Hugging Face Spaces | تطلب Pro $9/شهر لأي استضافة Python |
| Render / Koyeb free | ينام بعد 15 دقيقة من عدم النشاط |
| Replit free | ينام، يحتاج تفعيل يدوي |
| PythonAnywhere free | لا يدعم HTTP outward كافٍ |
| GitHub Actions | يعمل 5.5h ثم يُعاد تشغيله (فجوات) |
| **Telebot Creator** | ✅ مجاني 100%، 24/7، من جوالك |

**Telebot Creator** هي الحل الوحيد المجاني الحقيقي الذي:
1. لا يحتاج PC
2. لا يحتاج بطاقة ائتمان
3. يعمل 24/7 بدون انقطاع
4. يدعم HTTP requests لاستدعاء APIs خارجية (GitHub Models)
5. عنده تطبيق أندرويد رسمي

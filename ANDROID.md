# تشغيل Dolphin على أندرويد عبر Termux (بدون PC)

> المتطلبات: هاتف أندرويد بإصدار 9+ و **8GB RAM على الأقل** (لـ dolphin-llama3 8B Q4).
> إذا كان RAM أقل من 8GB، استخدم `dolphin-phi` (2.7B).

## 1) تثبيت Termux

1. نزّل **Termux** من F-Droid (لا تستخدم متجر Play، النسخة هناك قديمة):
   https://f-droid.org/packages/com.termux/

2. افتح Termux وشغّل:
```bash
pkg update && pkg upgrade -y
pkg install python git curl wget proot -y
```

## 2) تثبيت Ollama داخل Termux

```bash
# تثبيت Ollama (يعمل على aarch64)
curl -fsSL https://ollama.com/install.sh | sh

# تشغيل خدمة Ollama في الخلفية
ollama serve &
sleep 5

# تحميل Dolphin (ابدأ بالصغير إذا RAM أقل من 8GB)
ollama pull dolphin-llama3     # ~4.7GB، يحتاج 8GB RAM
# أو الأصغر:
# ollama pull dolphin-phi      # ~1.9GB، يحتاج 4GB RAM
```

## 3) تنزيل البوت

```bash
git clone https://github.com/ammma123312-netizen/dolphin-tg-bot.git
cd dolphin-tg-bot
pip install -r requirements.txt
```

## 4) ضبط التوكنات

```bash
cat > .env <<EOF
TELEGRAM_TOKEN=ضع_توكن_البوت_هنا
GH_TOKEN=
HF_TOKEN=
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=dolphin-llama3
EOF
```

## 5) تشغيل البوت

```bash
set -a && . ./.env && set +a
python app.py
```

الآن البوت يعمل على هاتفك. اذهب إلى تيليجرام على نفس الهاتف (أو أي جهاز) وتحدث مع `@Riwueh3e8hbot`.

## 6) تشغيل دائم (24/7) على الهاتف

لمنع Termux من الإغلاق:
- اضغط على إشعار Termux ← **Acquire wakelock**
- فعّل **Disable battery optimizations** لإعدادات Termux
- استخدم `termux-wake-lock`:
```bash
pkg install termux-api
termux-wake-lock
```

## ملاحظات
- ⚠️ سرعة الاستجابة على الهاتف تعتمد على المعالج. Snapdragon 8 Gen2+ يعطي ~10 tokens/sec، أقدم ببطء ملحوظ.
- ⚠️ البطارية تُستهلك بسرعة أثناء التشغيل.
- ⚠️ مساحة التخزين: dolphin-llama3 يحتاج ~5GB فارغة.
- 💡 **البديل الأسهل**: شغّل Ollama على PC، وتحكم بالبوت من تيليجرام على الهاتف. هذا أوضح وأسرع.

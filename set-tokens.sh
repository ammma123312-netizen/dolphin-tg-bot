#!/usr/bin/env bash
# ============================================================
# ضبط التوكنات كمتغيرات بيئة (محلياً)
# ============================================================
set -e

echo "=== ضبط التوكنات ==="

read -p "Telegram Bot Token: " TG_TOKEN
read -p "GitHub Token (اختياري، Enter للتخطي): " GH_TK
read -p "Hugging Face Token (اختياري، Enter للتخطي): " HF_TK

# إنشاء ملف .env
cat > .env <<EOF
TELEGRAM_TOKEN=$TG_TOKEN
GH_TOKEN=$GH_TK
HF_TOKEN=$HF_TK
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=dolphin-llama3
EOF

echo ""
echo "✅ تم حفظ التوكنات في .env"
echo "⚠️ لا تشارك ملف .env مع أحد ولا ترفعه لـ GitHub (موجود في .gitignore)"
echo ""
echo "لتحميل التوكنات قبل تشغيل البوت:"
echo "  export \$(cat .env | xargs)"
echo "أو شغّل ./run-bot.sh (يفعل ذلك تلقائياً)"

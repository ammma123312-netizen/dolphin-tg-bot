#!/usr/bin/env bash
# ============================================================
# تشغيل البوت محلياً
# ============================================================
set -e

echo "=== تشغيل Dolphin Bot ==="

# تحميل متغيرات البيئة من .env
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
  echo "✅ تم تحميل .env"
else
  echo "⚠️ لا يوجد ملف .env. شغّل ./set-tokens.sh أولاً."
  exit 1
fi

# فحص Ollama
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "⚠️ Ollama لا يعمل. سأحاول تشغيله..."
  if command -v ollama >/dev/null 2>&1; then
    ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
  fi
fi

# فحص Telegram token
if [ -z "$TELEGRAM_TOKEN" ]; then
  echo "❌ TELEGRAM_TOKEN غير مضبوط في .env"
  exit 1
fi

echo ""
echo "📡 الحالة:"
echo "  Ollama: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:11434/api/tags || echo 'لا يعمل')"
echo "  Telegram: متصل"
echo ""
echo "🚀 تشغيل البوت... (Ctrl+C للإيقاف)"
echo ""

exec python3 app.py

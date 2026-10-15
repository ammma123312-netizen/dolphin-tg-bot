#!/usr/bin/env bash
# ============================================================
# تثبيت Ollama + Dolphin + اعتماديات البوت
# يدعم: macOS / Linux / Windows (Git Bash أو WSL)
# ============================================================
set -e

echo "=== Dolphin Bot — تثبيت محلي ==="

# 1) كشف نظام التشغيل
OS="unknown"
case "$(uname -s)" in
  Darwin*) OS="macos" ;;
  Linux*)  OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
esac
ARCH=$(uname -m)
echo "نظام التشغيل: $OS | المعالج: $ARCH"

# 2) تثبيت Ollama إن لم يكن مثبتاً
if ! command -v ollama >/dev/null 2>&1; then
  echo ""
  echo "📥 تثبيت Ollama..."
  if [ "$OS" = "macos" ] || [ "$OS" = "linux" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
  elif [ "$OS" = "windows" ]; then
    echo "⚠️ على Windows: نزّل Ollama يدوياً من https://ollama.com/download"
    echo "   ثم أعد تشغيل هذا السكريبت."
    exit 1
  fi
else
  echo "✅ Ollama مثبت بالفعل: $(ollama --version 2>/dev/null || echo 'version unknown')"
fi

# 3) تشغيل خدمة Ollama (في الخلفية) إن لم تكن تعمل
echo ""
echo "🚀 التأكد من تشغيل خدمة Ollama..."
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  if [ "$OS" = "macos" ]; then
    open -a Ollama 2>/dev/null || ollama serve >/tmp/ollama.log 2>&1 &
  elif [ "$OS" = "linux" ]; then
    systemctl --user start ollama 2>/dev/null || ollama serve >/tmp/ollama.log 2>&1 &
  fi
  echo "⏳ انتظار بدء الخدمة..."
  for i in {1..15}; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then break; fi
    sleep 1
  done
fi

if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
  echo "✅ Ollama يعمل على http://localhost:11434"
else
  echo "❌ فشل بدء Ollama. شغّل يدوياً: ollama serve"
  exit 1
fi

# 4) تحميل نموذج Dolphin
echo ""
echo "🐬 تحميل نموذج Dolphin (dolphin-llama3، ~4.7GB)..."
echo "   قد يستغرق 5-15 دقيقة حسب سرعة الإنترنت."
ollama pull dolphin-llama3

echo ""
echo "🐬 (اختياري) تحميل dolphin-mistral (~4.1GB) كاحتياط..."
read -p "تنزيل الآن؟ [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  ollama pull dolphin-mistral
fi

echo ""
echo "🐬 (اختياري) تحميل dolphin-mixtral (~26GB، يحتاج 32GB RAM)..."
read -p "تنزيل؟ [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  ollama pull dolphin-mixtral
fi

# 5) تثبيت اعتماديات Python
echo ""
echo "📦 تثبيت اعتماديات Python..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ Python 3 غير مثبت. ثبّته من https://python.org"
  exit 1
fi
python3 -m pip install --user -r requirements.txt

# 6) اختبار سريع للنموذج
echo ""
echo "🧪 اختبار سريع للنموذج..."
ollama run dolphin-llama3 "قل مرحبا بالعربية في جملة واحدة" --verbose 2>&1 | head -10

echo ""
echo "✅ التثبيت اكتمل!"
echo ""
echo "الخطوة التالية:"
echo "  1. ضبط التوكنات (شغّل: ./set-tokens.sh)"
echo "  2. تشغيل البوت: ./run-bot.sh"

"""
Dolphin Telegram Bot
====================
بوت تيليجرام ذكي يعمل في السحابة عبر GitHub Actions (مجاني، بدون اشتراك).

النماذج (Inference):
  - أساسي: GitHub Models (https://models.inference.ai.azure.com)
    يستخدم توكن GitHub العادي (مجاني لمستخدمي GitHub، 150 طلب/يوم لكل نموذج).
  - احتياطي: HF Inference Router (يتطلب رصيد/Pro).

الميزات:
  - دردشة متعددة الأدوار لكل مستخدم (ذاكرة 24 رسالة).
  - بحث ويب عبر DuckDuckGo: /search
  - بحث + تلخيص بالذكاء الاصطناعي: /summary
  - اختيار النموذج: /models و /model N
  - مسح الذاكرة: /new

الأوامر: /start /help /new /search /summary /models /model /info
"""

import os
import re
import logging
import asyncio
from html import unescape
from typing import Dict, List
from urllib.parse import unquote

import requests
from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("dolphin-bot")

# ----------------------------------------------------------------------
# Secrets & configuration
# ----------------------------------------------------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# قائمة النماذج. الأولى مفضّلة (أكثر انفتاحاً)، والباقي يُجرّب عند الفشل.
# GitHub Models يدعم هذه الأسماء (تحقق من https://github.com/marketplace/models):
DEFAULT_MODELS = [
    "Mistral-Nemo",                    # مفتوح، أقل تصفية، دعم عربي جيد
    "Mistral-large",                   # قوي، مفتوح نسبياً
    "Meta-Llama-3.3-70B-Instruct",     # عام موثوق
    "Meta-Llama-3.1-70B-Instruct",     # احتياط لـ 70B
    "Mistral-7B-Instruct",             # احتياط صغير
    "Phi-3.5-mini-instruct",           # احتياط صغير جداً
    "gpt-4o-mini",                     # احتياط من OpenAI عبر GH Models
]

SYSTEM_PROMPT = (
    "You are Dolphin, a helpful, uncensored AI assistant. "
    "You answer directly and honestly without moralizing or unnecessary caveats. "
    "You are fluent in Arabic and English. "
    "When the user writes in Arabic, respond in Arabic unless explicitly asked otherwise. "
    "Be concise by default; elaborate only when asked."
)

MAX_HISTORY = 24
MAX_TOKENS = 1024
TEMPERATURE = 0.7

# ----------------------------------------------------------------------
# In-memory state
# ----------------------------------------------------------------------
conversations: Dict[int, List[dict]] = {}
user_models: Dict[int, str] = {}

def get_history(user_id: int) -> List[dict]:
    if user_id not in conversations:
        conversations[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return conversations[user_id]

def get_model(user_id: int) -> str:
    return user_models.get(user_id, DEFAULT_MODELS[0])

# ----------------------------------------------------------------------
# GitHub Models (OpenAI-compatible) — الأساسي
# ----------------------------------------------------------------------
GH_MODELS_URL = "https://models.inference.ai.azure.com/chat/completions"

def gh_models_chat(messages: List[dict], model: str) -> str:
    if not GH_TOKEN:
        raise RuntimeError("GH_TOKEN غير مضبوط.")
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "stream": False,
    }
    r = requests.post(GH_MODELS_URL, headers=headers, json=payload, timeout=90)
    if r.status_code != 200:
        raise RuntimeError(f"GH Models {r.status_code}: {r.text[:300]}")
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()

# ----------------------------------------------------------------------
# HF Inference Router — احتياطي
# ----------------------------------------------------------------------
HF_ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"

HF_FALLBACK_MODELS = [
    "NousResearch/Hermes-3-Llama-3.1-70B",
    "meta-llama/Llama-3.3-70B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
]

def hf_router_chat(messages: List[dict], model: str) -> str:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN غير مضبوط.")
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "stream": False,
    }
    r = requests.post(HF_ROUTER_URL, headers=headers, json=payload, timeout=90)
    if r.status_code != 200:
        raise RuntimeError(f"HF Router {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]["content"].strip()

# ----------------------------------------------------------------------
# موحّد: يجرب GitHub Models ثم HF Router
# ----------------------------------------------------------------------
def llm_chat(messages: List[dict], preferred_model: str) -> tuple:
    """يرجع (text, provider/model). يجرّب GitHub Models أولاً ثم HF Router."""
    last_err = None
    # 1) GitHub Models: الموديل المفضل ثم باقي القائمة
    chain = [preferred_model] + [m for m in DEFAULT_MODELS if m != preferred_model]
    for m in chain:
        try:
            txt = gh_models_chat(messages, m)
            return txt, f"github/{m}"
        except Exception as e:
            last_err = e
            log.warning("GitHub Models تخطّي %s: %s", m, str(e)[:160])
    # 2) HF Router (احتياطي)
    if HF_TOKEN:
        for m in HF_FALLBACK_MODELS:
            try:
                txt = hf_router_chat(messages, m)
                return txt, f"hf/{m}"
            except Exception as e:
                last_err = e
                log.warning("HF Router تخطّي %s: %s", m, str(e)[:160])
    raise RuntimeError(f"كل المزودين فشلوا. آخر خطأ: {last_err}")

# ----------------------------------------------------------------------
# بحث ويب (DuckDuckGo HTML — بدون مفتاح)
# ----------------------------------------------------------------------
def web_search(query: str, n: int = 5) -> List[dict]:
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120 Safari/537.36",
    }
    r = requests.post(url, data={"q": query}, headers=headers, timeout=20)
    r.raise_for_status()
    results: List[dict] = []
    # طريقة 1: regex شامل
    for block in re.findall(
        r'<a rel="nofollow" class="result__a"[^>]*>(.*?)</a>.*?'
        r'<a class="result__snippet"[^>]*>(.*?)</a>.*?'
        r'<a class="result__url"[^>]*>(.*?)</a>',
        r.text, re.S,
    ):
        title_html, snippet_html, url_html = block
        title = unescape(re.sub(r"<[^>]+>", "", title_html)).strip()
        snippet = unescape(re.sub(r"<[^>]+>", "", snippet_html)).strip()
        link = "https://" + unescape(re.sub(r"<[^>]+>", "", url_html)).strip()
        if title and link:
            results.append({"title": title, "url": link, "snippet": snippet})
        if len(results) >= n:
            return results
    # طريقة 2: fallback للروابط uddg=
    if not results:
        for m in re.finditer(r'<a class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r.text, re.S):
            link_raw = m.group(1)
            title = unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
            m2 = re.search(r"uddg=([^&]+)", link_raw)
            link = unquote(m2.group(1)) if m2 else link_raw
            if title and link:
                results.append({"title": title, "url": link, "snippet": ""})
            if len(results) >= n:
                break
    return results

# ----------------------------------------------------------------------
# Telegram handlers
# ----------------------------------------------------------------------
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\n"
        "أنا *Dolphin* — مساعد ذكي غير مقيد يعمل في السحابة.\n\n"
        "• راسلني بأي سؤال أو رسالة وأرد عليك.\n"
        "• استخدم /search <code>كلمة البحث</code> للبحث في الويب.\n"
        "• /summary <code>كلمة البحث</code> للبحث وتلخيص النتائج.\n"
        "• /models لعرض النماذج، /model <code>الرقم</code> للتبديل.\n"
        "• /new لبدء محادثة جديدة (مسح الذاكرة).\n"
        "• /help لكل الأوامر.",
        parse_mode=ParseMode.HTML,
    )

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *الأوامر المتاحة:*\n\n"
        "/start — ترحيب\n"
        "/new — محادثة جديدة (مسح الذاكرة)\n"
        "/search <code>query</code> — بحث ويب عبر DuckDuckGo\n"
        "/summary <code>query</code> — بحث ثم تلخيص بالذكاء الاصطناعي\n"
        "/models — قائمة النماذج\n"
        "/model <code>N</code> — اختيار النموذج رقم N\n"
        "/info — معلومات البوت الحالية\n",
        parse_mode=ParseMode.HTML,
    )

async def cmd_new(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    conversations.pop(uid, None)
    await update.message.reply_text("✅ بدأت محادثة جديدة. الذاكرة القديمة محيت.")

async def cmd_models(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    current = get_model(uid)
    lines = ["*النماذج المتاحة (عبر GitHub Models):*", ""]
    for i, m in enumerate(DEFAULT_MODELS, 1):
        mark = "✅ " if m == current else "   "
        lines.append(f"{mark}`{i}`. `{m}`")
    lines.append("\nللتبديل: /model <code>الرقم</code>")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)

async def cmd_model(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not ctx.args:
        await cmd_models(update, ctx)
        return
    try:
        n = int(ctx.args[0])
        if 1 <= n <= len(DEFAULT_MODELS):
            user_models[uid] = DEFAULT_MODELS[n - 1]
            await update.message.reply_text(
                f"✅ تم اختيار النموذج:\n<code>{user_models[uid]}</code>",
                parse_mode=ParseMode.HTML,
            )
        else:
            await update.message.reply_text("رقم خارج النطاق.")
    except ValueError:
        await update.message.reply_text("استخدم: /model <code>رقم</code>", parse_mode=ParseMode.HTML)

async def cmd_info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    msgs = get_history(uid)
    await update.message.reply_text(
        f"ℹ️ معلومات البوت:\n"
        f"• النموذج الحالي: <code>{get_model(uid)}</code>\n"
        f"• عدد الرسائل في الذاكرة: {len(msgs)}\n"
        f"• الحد الأقصى للذاكرة: {MAX_HISTORY}\n"
        f"• درجة الحرارة: {TEMPERATURE}\n"
        f"• Max tokens: {MAX_TOKENS}\n"
        f"• المزود الأساسي: GitHub Models\n"
        f"• المزود الاحتياطي: {'HF Router' if HF_TOKEN else 'غير مفعّل'}",
        parse_mode=ParseMode.HTML,
    )

async def cmd_search(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("استخدم: /search <code>كلمة البحث</code>", parse_mode=ParseMode.HTML)
        return
    query = " ".join(ctx.args)
    msg = await update.message.reply_text(f"🔍 أبحث عن: {query}...")
    try:
        results = await asyncio.to_thread(web_search, query, 5)
        if not results:
            await msg.edit_text("لا توجد نتائج.")
            return
        text_lines = [f"🔍 نتائج البحث عن: *{query}*", ""]
        for i, r in enumerate(results, 1):
            text_lines.append(f"{i}. [{r['title']}]({r['url']})")
            if r.get("snippet"):
                text_lines.append(f"   _{r['snippet'][:200]}_")
            text_lines.append("")
        await msg.edit_text("\n".join(text_lines), parse_mode=ParseMode.MARKDOWN,
                            disable_web_page_preview=True)
    except Exception as e:
        await msg.edit_text(f"خطأ في البحث: {e}")

async def cmd_summary(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not ctx.args:
        await update.message.reply_text("استخدم: /summary <code>كلمة البحث</code>", parse_mode=ParseMode.HTML)
        return
    query = " ".join(ctx.args)
    uid = update.effective_user.id
    msg = await update.message.reply_text(f"🔍 أبحث وألخّص: {query}...")
    try:
        results = await asyncio.to_thread(web_search, query, 5)
        if not results:
            await msg.edit_text("لا توجد نتائج للبحث.")
            return
        context_block = "\n\n".join(
            f"[{i+1}] {r['title']}\n{r['url']}\n{r.get('snippet','')}"
            for i, r in enumerate(results)
        )
        prompt = [
            {"role": "system", "content": "You summarize web search results concisely in the user's language."},
            {"role": "user", "content":
                f"Search query: {query}\n\nResults:\n{context_block}\n\n"
                f"Please give a concise summary in Arabic with key facts and the source numbers."},
        ]
        text, used = await asyncio.to_thread(llm_chat, prompt, get_model(uid))
        await msg.edit_text(
            f"🔍 *{query}*\n\n{text}\n\n_النموذج: {used}_",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    except Exception as e:
        await msg.edit_text(f"خطأ: {e}")

async def on_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text or ""
    if not text.strip():
        return
    history = get_history(uid)
    history.append({"role": "user", "content": text})
    if len(history) > MAX_HISTORY:
        history[:] = [history[0]] + history[-(MAX_HISTORY - 1):]

    sent = await update.message.reply_text("⏳ أفكّر...")
    try:
        reply, used = await asyncio.to_thread(llm_chat, history, get_model(uid))
        history.append({"role": "assistant", "content": reply})
        footer = f"\n\n_النموذج: {used}_" if used != f"github/{get_model(uid)}" else ""
        final = reply + footer
        for i in range(0, len(final), 4000):
            await update.message.reply_text(final[i:i+4000])
        try:
            await sent.delete()
        except Exception:
            pass
    except Exception as e:
        log.exception("chat failure")
        try:
            await sent.edit_text(f"⚠️ خطأ: {e}")
        except Exception:
            await update.message.reply_text(f"⚠️ خطأ: {e}")

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "ترحيب"),
        BotCommand("new", "محادثة جديدة"),
        BotCommand("search", "بحث ويب"),
        BotCommand("summary", "بحث + تلخيص"),
        BotCommand("models", "قائمة النماذج"),
        BotCommand("model", "اختيار نموذج"),
        BotCommand("info", "معلومات البوت"),
        BotCommand("help", "مساعدة"),
    ])
    log.info("Bot commands registered.")

def main():
    if not TELEGRAM_TOKEN:
        raise SystemExit("TELEGRAM_TOKEN غير مضبوط.")
    if not GH_TOKEN:
        raise SystemExit("GH_TOKEN غير مضبوط.")
    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .concurrent_updates(True)
        .build()
    )
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("new", cmd_new))
    app.add_handler(CommandHandler("models", cmd_models))
    app.add_handler(CommandHandler("model", cmd_model))
    app.add_handler(CommandHandler("info", cmd_info))
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CommandHandler("summary", cmd_summary))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    log.info("Starting polling...")
    app.run_polling(drop_pending_updates=False, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()


import os
import requests
import json
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Environment Variables से API Keys लें
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# /start कमांड हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('नमस्ते! मैं GROK-3 AI बोट हूँ! 🤖')

# यूजर के मैसेज को प्रोसेस करें
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        
        # GROK-3 API को कॉल करें
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://api.telegram.org",
                "X-Title": "Telegram Grok Bot"
            },
            data=json.dumps({
                "model": "x-ai/grok-3-beta",
                "messages": [{"role": "user", "content": user_message}]
            })
        )
        
        ai_response = response.json()['choices'][0]['message']['content']
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f'⚠️ त्रुटि: {str(e)}')

# HTTP सर्वर और Telegram बोट को एक साथ चलाएं
async def main():
    # HTTP सर्वर सेटअप
    app = web.Application()
    app.router.add_get('/', lambda request: web.Response(text="✅ Bot चल रहा है!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    await site.start()
    
    # Telegram बोट शुरू करें
    telegram_app = Application.builder().token(TELEGRAM_API_KEY).build()
    telegram_app.add_handler(CommandHandler('start', start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await telegram_app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

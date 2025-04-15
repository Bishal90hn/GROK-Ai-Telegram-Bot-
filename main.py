
import os
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_API_KEY, OPENROUTER_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('नमस्ते! मैं Grok-3 AI बोट हूँ। आप मुझसे कुछ भी पूछ सकते हैं!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
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
        await update.message.reply_text(f'त्रुटि हुई: {str(e)}')

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_API_KEY).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Webhook Configuration
    PORT = int(os.environ.get("PORT", 10000))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url="https://your-app-name.onrender.com/" + TELEGRAM_API_KEY
    )

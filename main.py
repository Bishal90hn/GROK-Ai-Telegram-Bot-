
import os
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Environment Variables से API Keys लें
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# स्टार्ट कमांड हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('नमस्ते! मैं GROK-3 AI बोट हूँ, आप मुझसे कुछ भी पूछ सकते हैं! 🤖')

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
        
        # जवाब पाएं और भेजें
        ai_response = response.json()['choices'][0]['message']['content']
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f'⚠️ त्रुटि: {str(e)}')

# Telegram बोट एप्लिकेशन सेटअप करें
app = Application.builder().token(TELEGRAM_API_KEY).build()

# कमांड और मैसेज हैंडलर जोड़ें
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# मुख्य प्रोग्राम शुरू करें
if __name__ == "__main__":
    print("✅ बोट चल रहा है...")
    app.run_polling()  # Polling मेथड का उपयोग करें


import os
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Render के Environment Variables से API Keys लें
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# /start कमांड का जवाब देने के लिए फंक्शन
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('नमस्ते! मैं GROK-3 AI बोट हूँ, कुछ भी पूछें! 🤖')

# यूजर के मैसेज को प्रोसेस करने वाला फंक्शन
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text
        
        # GROK-3 API को कॉल करें (Syntax Error Fixed)
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
        )  # यहाँ closing bracket जोड़ा गया है
        
        # AI का जवाब पाएं और भेजें
        ai_response = response.json()['choices'][0]['message']['content']
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f'⚠️ त्रुटि: {str(e)}')

# Telegram बोट एप्लिकेशन बनाएं
app = Application.builder().token(TELEGRAM_API_KEY).build()

# कमांड और मैसेज हैंडलर रजिस्टर करें
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# पोलिंग मेथड से बोट स्टार्ट करें
if __name__ == "__main__":
    print("✅ बोट सक्रिय है!")
    app.run_polling()

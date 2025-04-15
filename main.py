
import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"]["text"]

    # GROK 3 (OpenRouter) से जवाब लेना
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "x-ai/grok-3-beta",
            "messages": [{"role": "user", "content": user_message}]
        })
    )

    result = response.json()
    try:
        reply = result["choices"][0]["message"]["content"]
    except Exception as e:
        reply = "माफ़ कीजिए, कुछ गड़बड़ हो गई है।"

    send_message(chat_id, reply)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is live!"

# Render के लिए पोर्ट bind करना जरूरी है
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

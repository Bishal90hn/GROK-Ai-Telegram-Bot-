import requests
import json
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"
OPENROUTER_API_KEY = "<YOUR_GROK_API_KEY>"

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

    answer = response.json()["choices"][0]["message"]["content"]
    send_message(chat_id, answer)
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is live!"

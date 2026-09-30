"""Omnichannel Reply Assistant - drafts customer replies for SMS / WhatsApp / Email.
Works offline (rule-based mode) and uses Claude when ANTHROPIC_API_KEY is set."""
import os
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")

CHANNEL_RULES = {
    "sms": {"limit": 160, "style": "very short, plain text, no emojis"},
    "whatsapp": {"limit": 400, "style": "friendly, conversational, at most one emoji"},
    "email": {"limit": 1200, "style": "polite and formal, with greeting and sign-off"},
}

INTENTS = {
    "refund": ["refund", "money back", "charged twice"],
    "delivery": ["delivery", "order", "shipping", "not arrived", "late"],
    "login": ["password", "login", "log in", "otp", "locked"],
    "billing": ["invoice", "bill", "payment", "price"],
}

TEMPLATES = {
    "refund": "We're sorry about this. Your refund request is logged and will be processed in 5-7 working days.",
    "delivery": "Thanks for reaching out. We're checking your order status and will update you shortly.",
    "login": "Please reset your password using the 'Forgot password' link. If it still fails, reply here for help.",
    "billing": "Thanks for your message. We'll share the billing details with you shortly.",
    "general": "Thanks for contacting us. Our team will get back to you shortly.",
}


def detect_intent(text: str) -> str:
    t = text.lower()
    for intent, words in INTENTS.items():
        if any(w in t for w in words):
            return intent
    return "general"


def rule_based_reply(text: str, channel: str) -> str:
    body = TEMPLATES[detect_intent(text)]
    if channel == "email":
        return f"Dear Customer,\n\n{body}\n\nRegards,\nSupport Team"
    if channel == "whatsapp":
        return f"Hi! {body} 🙂"
    return body


def claude_reply(text: str, channel: str) -> str:
    rules = CHANNEL_RULES[channel]
    prompt = (
        f"You are a customer support agent. Write a reply to the customer message below.\n"
        f"Channel: {channel}. Style: {rules['style']}. Max {rules['limit']} characters.\n"
        f"Reply with the message text only.\n\nCustomer message:\n{text}"
    )
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": MODEL, "max_tokens": 500, "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["content"][0]["text"].strip()


@app.post("/api/reply")
def reply():
    data = request.get_json(silent=True) or {}
    text = (data.get("message") or "").strip()
    channel = data.get("channel", "sms")
    if not text or channel not in CHANNEL_RULES:
        return jsonify(error="Provide a message and a valid channel (sms/whatsapp/email)."), 400
    mode = "rule-based"
    try:
        if API_KEY:
            out, mode = claude_reply(text, channel), "claude"
        else:
            out = rule_based_reply(text, channel)
    except requests.RequestException:
        out = rule_based_reply(text, channel)  # graceful fallback
    limit = CHANNEL_RULES[channel]["limit"]
    return jsonify(intent=detect_intent(text), mode=mode, reply=out[:limit], length=len(out[:limit]), limit=limit)


@app.get("/")
def home():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)

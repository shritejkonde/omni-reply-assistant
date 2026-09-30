# Omnichannel Reply Assistant

A Flask + JavaScript web app that drafts customer-support replies for **SMS, WhatsApp and Email**. Each reply follows the length limit and tone of its channel.

## Features
- Detects customer intent: refund, delivery, login, billing or general
- Channel-aware replies:
  - **SMS**: max 160 characters, plain text
  - **WhatsApp**: friendly, conversational
  - **Email**: formal, with greeting and sign-off
- Uses **Claude** (Anthropic API) when `ANTHROPIC_API_KEY` is set
- Falls back to rule-based replies if no key is set or the API call fails

## Tech Stack
Python, Flask, JavaScript, HTML/CSS, Anthropic API

## Project Structure
```
omni-reply-assistant/
├── app.py            # Flask backend + API logic
├── static/
│   └── index.html    # Frontend UI
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works
1. The user pastes a customer message and selects a channel.
2. The frontend sends it to `POST /api/reply`.
3. The backend detects the intent and builds the reply, using Claude if a key is available, otherwise templates.
4. The reply is trimmed to the channel's limit and returned with its intent, mode and length.

## Setup
```bash
git clone https://github.com/<your-username>/omni-reply-assistant.git
cd omni-reply-assistant
pip install -r requirements.txt
```

Optional, to enable Claude:
```bash
# Linux / macOS
export ANTHROPIC_API_KEY=your_key
# Windows (cmd)
set ANTHROPIC_API_KEY=your_key
```

Run:
```bash
python app.py
```
Open http://127.0.0.1:5000

## API
**POST** `/api/reply`

Request:
```json
{ "message": "My order has not arrived", "channel": "sms" }
```

Response:
```json
{
  "intent": "delivery",
  "mode": "rule-based",
  "reply": "Thanks for reaching out. We're checking your order status and will update you shortly.",
  "length": 86,
  "limit": 160
}
```

## Future Improvements
- Send replies through a real SMS/WhatsApp API
- Conversation history
- Multi-language replies

## Author
**Shritej Konde**: B.E. Electronics & Telecommunication, Sinhgad Institute of Technology

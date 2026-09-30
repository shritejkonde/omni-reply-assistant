# Omnichannel Reply Assistant

A small Flask web app that drafts customer-support replies for **SMS, WhatsApp and Email**, respecting each channel's length and tone.

## Features
- Detects customer intent (refund, delivery, login, billing, general)
- Channel-aware replies (SMS 160 chars, WhatsApp friendly, Email formal)
- Uses **Claude** via the Anthropic API when `ANTHROPIC_API_KEY` is set
- Falls back to rule-based replies when no key is set or the API fails

## Tech
Python, Flask, JavaScript, HTML/CSS, Anthropic API

## Run locally
```bash
pip install -r requirements.txt
# optional: enable Claude
export ANTHROPIC_API_KEY=your_key      # Windows: set ANTHROPIC_API_KEY=your_key
python app.py
```
Open http://127.0.0.1:5000

## API
`POST /api/reply` with `{"message": "...", "channel": "sms|whatsapp|email"}`

## Future work
Real SMS/WhatsApp sending through a communications API, conversation history, multi-language replies.

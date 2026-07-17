# AI Concierge MVP

AI Concierge MVP is a FastAPI-based assistant for hospitality businesses that helps guests with common requests, captures basic lead context, and supports a simple escalation flow. The current build focuses on a lightweight chat experience for hotels, resorts, and short-term rentals.

## Status
🚧 Early development — capstone project.

## What it does
- Responds to guest questions about food, transport, bookings, hotel services, and local info
- Uses simple intent detection to route requests
- Maintains basic in-session memory per user
- Exposes a REST chat endpoint for integration

## Core MVP features
- Chat interface for guests
- Intent-based response routing
- In-session conversation memory
- Basic conversational flow for common concierge requests

## Tech stack
- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- python-dotenv

## Project structure
```text
app/
  main.py
  routes/
    chat.py
  schemas/
    chat_schema.py
  services/
    intent_service.py
    memory_service.py
    response_service.py
```

## Getting started

### 1. Prerequisites
- Python 3.10 or later
- pip

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.
You can also view the interactive docs at http://127.0.0.1:8000/docs.

## Example request
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"guest-1","message":"I need a taxi to the airport"}'
```

The response includes the user ID, the original message, the detected intent, and the generated response.

## Notes
- The current MVP uses rule-based intent detection rather than a large language model.
- Conversation memory is currently stored in memory for the active process.

## Roadmap
- Add persistent storage for conversations and leads
- Integrate a real AI model or retrieval-based knowledge base
- Support lead capture and human handoff workflows
- Add authentication and deployment configuration

## License
MIT — see [LICENSE](./LICENSE)

# AI Writing Copilot

Full-stack **AI writing assistant** for rewriting text, adjusting tone, fixing grammar, and drafting emails.

Built for mid-level full-stack interviews. Shows practical LLM integration, auth, document history, and a clean API design.

---

## Features

- [x] User authentication (JWT)
- [x] Rewrite text (improve clarity, fix grammar)
- [x] Tone adjustment (professional, casual, friendly, formal, concise)
- [x] Email draft generation from bullet points / intent
- [x] Expand or shorten text
- [x] Writing session history (save prompts + outputs)
- [x] Docker Compose + Postgres
- [x] FastAPI backend with dedicated AI service layer
- [ ] Next.js frontend UI (scaffold ready)
- [ ] Streaming responses (easy extension)

---

## Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | FastAPI + Python 3.11+             |
| AI       | OpenAI API (chat models)           |
| Database | PostgreSQL + SQLAlchemy            |
| Auth     | JWT                                |
| Frontend | Next.js 15 + TypeScript (scaffold) |
| Infra    | Docker Compose                     |

---

## Architecture

```
User → Next.js Frontend
         ↓
      FastAPI Backend
         ├── Auth (JWT)
         ├── Writing sessions (history)
         └── AI service (rewrite, tone, email, expand/shorten)
         ↓
      PostgreSQL + OpenAI
```

---

## API Overview

| Method | Endpoint                         | Description                          |
|--------|----------------------------------|--------------------------------------|
| POST   | `/api/v1/auth/register`          | Register                             |
| POST   | `/api/v1/auth/login`             | Login                                |
| GET    | `/api/v1/auth/me`                | Current user                         |
| POST   | `/api/v1/write/rewrite`          | Improve / fix grammar                |
| POST   | `/api/v1/write/tone`             | Change tone                          |
| POST   | `/api/v1/write/email`            | Draft an email                       |
| POST   | `/api/v1/write/transform`        | Expand or shorten text               |
| GET    | `/api/v1/sessions/`              | List writing history                 |
| GET    | `/api/v1/sessions/{id}`          | Get one session                      |
| DELETE | `/api/v1/sessions/{id}`          | Delete a session                     |

---

## Getting Started

```bash
git clone https://github.com/Invenitur42/ai-writing-copilot.git
cd ai-writing-copilot
docker-compose up -d

cd backend
cp .env.example .env   # set OPENAI_API_KEY + SECRET_KEY
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

---

## Example requests

**Rewrite**
```json
POST /api/v1/write/rewrite
{ "text": "i think we should maybe meet next week if ur free" }
```

**Tone**
```json
POST /api/v1/write/tone
{ "text": "Can you send the report today?", "tone": "professional" }
```

**Email**
```json
POST /api/v1/write/email
{
  "intent": "Follow up on interview, restate interest in backend role",
  "recipient": "hiring manager",
  "tone": "professional"
}
```

---

## Interview Talking Points

- Prompt design per writing mode (rewrite vs tone vs email)
- Saving user history without storing unnecessary PII
- Separating AI service from HTTP layer for testability
- Cost and latency trade-offs of LLM calls in a product API
- How you would add streaming and rate limiting next

---

Part of the [AI Tools Portfolio](https://github.com/Invenitur42/ai-tools-portfolio).
# Writing & Mail AI

API for rewriting text, changing tone, drafting short emails, and expanding/shortening copy. Keeps a history of runs per user.

**FastAPI · Postgres · OpenAI**

(Frontend is only a light Next.js scaffold for now.)

---

## Endpoints

| Method | Path | What it does |
|--------|------|----------------|
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Current user |
| POST | `/api/v1/write/rewrite` | Clean up / improve text |
| POST | `/api/v1/write/tone` | Rewrite in a given tone |
| POST | `/api/v1/write/email` | Draft an email from notes |
| POST | `/api/v1/write/transform` | Expand or shorten |
| GET | `/api/v1/sessions/` | Recent history |
| DELETE | `/api/v1/sessions/{id}` | Delete one entry |

---

## Run

```bash
git clone https://github.com/Invenitur42/Writing_n_Mail_ai.git
cd Writing_n_Mail_ai
docker compose up -d

cd backend
cp .env.example .env   # OPENAI_API_KEY, SECRET_KEY
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

Docs: http://localhost:8000/docs

Example:

```json
POST /api/v1/write/tone
{ "text": "Can you send the report today?", "tone": "professional" }
```

---

## Implementation notes

Writing modes live in `app/services/writer.py` so the routes stay thin. Each call is stored as a session row if you want to look back later. Streaming and rate limits would be the obvious next pieces.

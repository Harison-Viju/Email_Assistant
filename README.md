AI-Powered Communication Assistant

Overview
This project ingests support emails, prioritizes them, analyzes sentiment, extracts key info, drafts empathetic replies using RAG + LLM, and provides a dashboard for review and sending.

Tech Stack
- Backend: FastAPI, SQLAlchemy (SQLite)
- AI: TF-IDF retrieval over CSV + OpenAI (optional, fallback heuristic)
- Email: IMAP fetch, SMTP send
- Frontend: Streamlit dashboard

Setup
1) Python 3.10+
2) Create .env in project root:
   IMAP_HOST=imap.gmail.com
   IMAP_USER=you@example.com
   IMAP_PASSWORD=app_password
   IMAP_FOLDER=INBOX
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=you@example.com
   SMTP_PASSWORD=app_password
   OPENAI_API_KEY=sk-...
   MODEL_NAME=gpt-4o-mini
   KNOWLEDGE_CSV_PATH=68b1acd44f393_Sample_Support_Emails_Dataset.csv

3) Install dependencies:
   pip install -r requirements.txt

Run Backend
uvicorn backend.app.main:app --reload --port 8000

Run Dashboard
streamlit run backend/app/dashboard.py

API Endpoints
- GET /health
- GET /api/emails/ (list ordered by urgency and recency)
- POST /api/emails/ (create manual email)
- POST /api/emails/ingest (fetch from IMAP + analyze)
- POST /api/emails/{id}/analyze (reanalyze)
- POST /api/emails/{id}/draft (generate reply draft)
- POST /api/emails/{id}/send (send reply via SMTP)
- GET /api/emails/stats (summary counts)

Notes
- If OpenAI key is not set, drafts are generated heuristically.
- Retrieval indexes the provided CSV to add similar-past-ticket context.

Demo Script (suggested)
1) Start backend and dashboard.
2) Click Ingest Emails.
3) Select an email, view extracted info and analytics.
4) Draft reply and (optionally) send.



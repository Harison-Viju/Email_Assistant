# Setup Instructions for AI-Powered Communication Assistant

## 1. Environment Setup

Create a `.env` file in the project root with the following content:

```env
# Email Configuration (IMAP for fetching emails)
IMAP_HOST=imap.gmail.com
IMAP_USER=your_email@gmail.com
IMAP_PASSWORD=your_app_password
IMAP_FOLDER=INBOX

# Email Configuration (SMTP for sending emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# AI Configuration (Optional - will use fallback if not provided)
OPENAI_API_KEY=sk-your_openai_api_key_here
MODEL_NAME=gpt-4o-mini

# Knowledge Base
KNOWLEDGE_CSV_PATH=68b1acd44f393_Sample_Support_Emails_Dataset.csv

# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./emails.db
```

## 2. Gmail Setup (if using Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in your `.env` file

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Application

### Option A: Run Backend Only
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### Option B: Run Dashboard (Recommended)
```bash
streamlit run backend/app/dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## 5. Test the Application

1. Open the Streamlit dashboard
2. Click "Ingest Emails" to fetch emails from your IMAP account
3. View the analytics and email list
4. Select an email to see analysis and draft replies
5. Test the "Draft Reply" and "Send Reply" functionality

## 6. API Endpoints

If you want to test the API directly:

- **Health Check**: `GET http://localhost:8000/health`
- **List Emails**: `GET http://localhost:8000/api/emails/`
- **Ingest Emails**: `POST http://localhost:8000/api/emails/ingest`
- **Analyze Email**: `POST http://localhost:8000/api/emails/{id}/analyze`
- **Draft Reply**: `POST http://localhost:8000/api/emails/{id}/draft`
- **Send Reply**: `POST http://localhost:8000/api/emails/{id}/send`
- **Get Stats**: `GET http://localhost:8000/api/emails/stats`

## 7. Features

- ✅ Email filtering (Support, Query, Request, Help)
- ✅ Sentiment analysis (Positive/Negative/Neutral)
- ✅ Priority detection (Urgent/Not Urgent)
- ✅ Information extraction (contacts, requirements, indicators)
- ✅ RAG-based knowledge retrieval from CSV
- ✅ AI-powered reply generation (OpenAI or fallback)
- ✅ Email sending via SMTP
- ✅ Interactive dashboard with analytics
- ✅ Priority queue for urgent emails

## 8. Troubleshooting

- If IMAP/SMTP fails: Check your email credentials and app password
- If OpenAI fails: The system will use a fallback heuristic for reply generation
- If dashboard doesn't load: Make sure the backend is running on port 8000
- If CSV not found: Ensure the CSV file is in the project root directory


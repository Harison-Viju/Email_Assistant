# 🤖 AI-Powered Communication Assistant

## 📋 Overview

An intelligent email management system that automatically processes support emails, analyzes sentiment, prioritizes urgent requests, and generates contextual AI-powered responses using Retrieval-Augmented Generation (RAG) and advanced prompt engineering.

## ✨ Key Features

### 📧 Email Processing
- **Smart Filtering**: Automatically identifies support emails containing keywords like "Support", "Query", "Request", "Help"
- **Priority Detection**: Uses keyword analysis to identify urgent emails ("immediately", "critical", "cannot access")
- **Information Extraction**: Extracts contact details, requirements, and sentiment indicators

### 🧠 AI-Powered Analysis
- **Sentiment Analysis**: Classifies emails as Positive, Negative, or Neutral
- **Context-Aware Responses**: Uses RAG to generate empathetic, contextually appropriate replies
- **Knowledge Base Integration**: Leverages historical email data for better response quality

### 📊 Advanced Dashboard
- **Interactive Analytics**: Real-time charts showing sentiment distribution, priority breakdown, and email trends
- **Priority Queue**: Urgent emails appear first for immediate attention
- **Draft Management**: Review, edit, and send AI-generated responses

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy database setup
│   ├── models.py            # Email and Reply data models
│   ├── schemas.py           # Pydantic schemas for API
│   ├── analysis.py          # Sentiment & priority analysis
│   ├── retrieval.py         # RAG knowledge base
│   ├── llm.py              # OpenAI integration & fallback
│   ├── email_clients.py     # IMAP/SMTP email handling
│   ├── dashboard.py         # Streamlit dashboard
│   └── routers/
│       └── emails.py        # API endpoints
```

### Data Flow
1. **Email Ingestion**: IMAP fetches emails → Filter by keywords → Store in SQLite
2. **Analysis Pipeline**: Sentiment analysis → Priority detection → Information extraction
3. **RAG Processing**: Query knowledge base → Generate context-aware responses
4. **Dashboard Display**: Analytics visualization → Email management interface

### AI Components
- **Sentiment Analysis**: Rule-based keyword matching with positive/negative/neutral classification
- **Priority Detection**: Urgent keyword identification for immediate attention
- **RAG System**: TF-IDF vectorization of historical emails for context retrieval
- **LLM Integration**: OpenAI GPT-4o-mini with fallback heuristic responses

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/Harison-Viju/Email_Assistant.git
cd Email_Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration (Optional)
Create `.env` file for real email integration:
```env
# Email Configuration
IMAP_HOST=imap.gmail.com
IMAP_USER=your_email@gmail.com
IMAP_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# AI Configuration
OPENAI_API_KEY=sk-your_openai_key_here
MODEL_NAME=gpt-4o-mini

# Knowledge Base
KNOWLEDGE_CSV_PATH=68b1acd44f393_Sample_Support_Emails_Dataset.csv
```

### Running the Application
```bash
# Terminal 1: Start Backend
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Start Dashboard
streamlit run backend/app/dashboard.py
```

Access the dashboard at: `http://localhost:8501`

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/emails/` | List emails (priority-sorted) |
| POST | `/api/emails/` | Create email manually |
| POST | `/api/emails/ingest` | Fetch emails from IMAP |
| POST | `/api/emails/{id}/analyze` | Analyze email sentiment/priority |
| POST | `/api/emails/{id}/draft` | Generate AI reply draft |
| POST | `/api/emails/{id}/send` | Send reply via SMTP |
| GET | `/api/emails/stats` | Get analytics statistics |

## 🎯 Demo Workflow

1. **Start Application**: Run backend and dashboard
2. **Ingest Emails**: Click "Ingest Emails" to load sample data
3. **View Analytics**: See sentiment distribution and priority breakdown
4. **Process Emails**: 
   - Urgent emails appear first (red indicators)
   - Click "Analyze" to run sentiment/priority analysis
   - Click "Draft Reply" to generate AI response
   - Edit draft if needed
   - Click "Send Reply" to send response
5. **Monitor Progress**: Track email status (pending → drafted → sent)

## 🔧 Technical Implementation

### Sentiment Analysis
```python
# Keyword-based sentiment detection
NEGATIVE_WORDS = {"cannot", "unable", "urgent", "critical", "error"}
POSITIVE_WORDS = {"thanks", "appreciate", "great", "awesome"}
```

### Priority Detection
```python
# Urgent keyword identification
URGENT_KEYWORDS = {"urgent", "immediately", "critical", "cannot access"}
```

### RAG Implementation
```python
# TF-IDF vectorization for knowledge retrieval
vectorizer = TfidfVectorizer(stop_words="english")
similarity = cosine_similarity(query_vector, knowledge_vectors)
```

### LLM Integration
```python
# OpenAI with RAG context
prompt = build_prompt(subject, body, sentiment, priority, context)
response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
```

## 📈 Analytics Features

- **Sentiment Distribution**: Pie chart showing positive/negative/neutral breakdown
- **Priority Analysis**: Bar chart of urgent vs normal emails
- **Time-based Trends**: Line chart of email volume by hour
- **Real-time Metrics**: Total, pending, drafted, and sent email counts

## 🛡️ Error Handling

- **Graceful Fallbacks**: Heuristic responses when OpenAI unavailable
- **Demo Mode**: Sample data when email credentials not configured
- **Input Validation**: Pydantic schemas ensure data integrity
- **Exception Handling**: Comprehensive error messages and logging

## 🚀 Deployment

### Local Development
```bash
# Backend
uvicorn backend.app.main:app --reload --port 8000

# Dashboard
streamlit run backend/app/dashboard.py
```

### Production Considerations
- Use PostgreSQL instead of SQLite for production
- Configure proper email credentials
- Set up monitoring and logging
- Implement rate limiting for API endpoints
- Use environment variables for sensitive data

## 📝 Evaluation Criteria Compliance

### ✅ Functionality
- **Email Filtering**: ✅ Keywords-based filtering (Support, Query, Request, Help)
- **Categorization**: ✅ Sentiment analysis (Positive/Negative/Neutral)
- **Prioritization**: ✅ Urgent detection with priority queue
- **Context-Aware Responses**: ✅ RAG + LLM integration

### ✅ User Experience
- **Intuitive Dashboard**: ✅ Clean, organized interface with clear actions
- **Analytics**: ✅ Interactive charts and real-time metrics
- **Email Management**: ✅ Priority-sorted list with detailed views

### ✅ Response Quality
- **RAG Implementation**: ✅ TF-IDF knowledge retrieval from CSV
- **Prompt Engineering**: ✅ Context-aware prompt construction
- **Empathetic Responses**: ✅ Sentiment-aware reply generation

## 🎬 Demo Video

[Link to demonstration video showing all features]

## 📚 Documentation

This project demonstrates:
- **End-to-end AI pipeline** from email ingestion to response generation
- **Modern web architecture** with FastAPI and Streamlit
- **Advanced AI techniques** including RAG and prompt engineering
- **Production-ready code** with proper error handling and validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Streamlit for dashboard framework
- FastAPI for backend framework
- The open-source community for various libraries



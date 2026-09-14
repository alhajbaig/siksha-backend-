# SikshaSaathi — Backend Architecture & API Layer

FastAPI server providing endpoints for **Authentication**, **3-Pane RAG Knowledge Retrieval**, **Socratic AI Dialogue**, and **Student Concept Telemetry**.

---

## Architecture Overview

```
backend/
├── main.py                  # Server entry point & static frontend mounting
├── config.py                # Environment and configuration settings
├── requirements.txt         # Python dependencies
├── routes/                  # API Endpoint controllers
│   ├── auth.py              # /api/auth (Login, Signup, JWT)
│   ├── rag.py               # /api/rag (Upload, Notes, Semantic Query)
│   ├── mentor.py            # /api/mentor (Socratic reasoning chat)
│   └── student.py           # /api/student (Telemetry & practice)
├── services/                # Business logic & AI algorithms
│   ├── rag_service.py       # Chunking & vector citation retrieval
│   └── socratic_service.py  # Socratic inquiry prompts & mode router
└── models/                  # Pydantic data schemas
    ├── user_model.py        # User & Auth schemas
    └── note_model.py        # Notes, chunks & citation schemas
```

---

## Setup & Running

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Run the Development Server
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Interactive Swagger API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **Mounted Frontend**: `http://localhost:8000/`

---

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status |
| `POST` | `/api/auth/login` | User authentication & JWT generation |
| `POST` | `/api/auth/signup` | Student / Teacher registration |
| `GET` | `/api/rag/notes` | Get all indexed RAG documents |
| `GET` | `/api/rag/notes/{id}` | Get document content & semantic chunks |
| `POST` | `/api/rag/query` | Grounded semantic vector query with citations |
| `POST` | `/api/rag/upload` | Ingest PDF / scan / note through 4-stage pipeline |
| `POST` | `/api/mentor/chat` | Socratic inquiry AI reasoning |
| `GET` | `/api/student/telemetry` | Concept confidence vectors & study stats |
| `POST` | `/api/student/practice/verify` | Verify mathematical problem with steps |

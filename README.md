# 🚀 SikshaSaathi — Backend API Deployment Package

This repository contains the standalone, production-ready FastAPI backend for **SikshaSaathi (शिक्षा साथी)**.
It provides educational AI mentors, automated syllabus-aligned revision, NCERT resource indexing, dual-engine authentication (Supabase Cloud PostgreSQL + SQLite resilience), classroom management, and real-time assessments.

---

## 🌟 Key Features
- **FastAPI Core**: Async, high-performance REST API with interactive Swagger docs at `/docs`.
- **Dual-Database Persistence**:
  - **Primary**: Supabase Cloud PostgreSQL for all persistent user profiles, classroom analytics, notes, and quiz submissions.
  - **Fallback**: Local SQLite layer ensuring continuous zero-downtime operation during cloud connectivity spikes.
- **Dynamic CORS**: Pre-configured with wildcard regex origin matching and explicit `FRONTEND_URL` support, enabling secure cross-origin requests from any Vercel, Netlify, or custom domain.
- **Multi-Modal AI Integration**: Groq Llama-3.3 70B & 8B for fast student mentorship, revision generation, and quiz creation.

---

## 📁 Repository Structure
```
backend_deploy/
├── Dockerfile              # Multi-stage production container image
├── Procfile                # Heroku / Dokku / Railway process definition
├── fly.toml                # Fly.io deployment manifest
├── render.yaml             # Render infrastructure-as-code Blueprint
├── requirements.txt        # Production Python dependencies
├── main.py                 # ASGI entrypoint for uvicorn
├── .env.example            # Template for environment variables
├── backend/                # Application source code
│   ├── config.py           # Environment and settings configuration
│   ├── db.py               # Database layer (PostgreSQL + SQLite)
│   ├── main.py             # FastAPI app initialization & CORS middleware
│   ├── models/             # Pydantic schemas and models
│   ├── routes/             # API route handlers
│   ├── services/           # AI, Supabase, curriculum, and notes services
│   └── data/               # Curriculum definitions and local DB seed
└── resources/              # NCERT and curriculum resource PDFs
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` or set these in your cloud provider's dashboard:

| Variable | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | Yes | App runtime mode | `production` |
| `PORT` | Optional | Port for the HTTP server (default: `8000`) | `8000` |
| `FRONTEND_URL` | Recommended | Live URL of your deployed frontend (e.g., Vercel) | `https://sikshasaathi.vercel.app` |
| `CORS_ORIGINS` | Optional | Additional allowed CORS origins | `http://localhost:3000,http://localhost:8000` |
| `GROQ_API_KEY` | Recommended | Groq API Key for AI Mentor & Quizzes | `gsk_...` |
| `SUPABASE_URL` | Recommended | Supabase Project URL | `https://xyz.supabase.co` |
| `SUPABASE_ANON_KEY` | Recommended | Supabase public anonymous key | `eyJhb...` |
| `SUPABASE_SERVICE_ROLE_KEY` | Recommended | Supabase service role secret | `eyJhb...` |
| `SUPABASE_DB_HOST` | Recommended | Supabase PostgreSQL direct host | `db.xyz.supabase.co` |
| `SUPABASE_DB_PORT` | Optional | Supabase PostgreSQL port | `5432` |
| `SUPABASE_DB_USER` | Recommended | Database user (typically `postgres`) | `postgres` |
| `SUPABASE_DB_PASSWORD` | Recommended | Database password | `your-db-password` |
| `JWT_SECRET` | Recommended | Random secret string for signing tokens | `a-strong-random-secret-key` |

---

## 🚀 Deployment Options

### Option 1: Deploy to Render (Recommended Free/Starter)

#### Method A: Using `render.yaml` (Render Blueprint)
1. Push this `backend_deploy` repository to GitHub or GitLab.
2. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Blueprint**.
3. Connect your repository. Render automatically reads `render.yaml` and provisions the Web Service.
4. Fill in the secret environment variables (`GROQ_API_KEY`, `SUPABASE_DB_PASSWORD`, etc.) in the dashboard prompt.
5. Click **Apply**.

#### Method B: Manual Web Service on Render
1. Click **New +** -> **Web Service**.
2. Connect your repository.
3. Configure the following settings:
   - **Name**: `sikshasaathi-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 2`
   - **Instance Type**: `Free`
4. Under **Advanced** -> **Environment Variables**, add the variables from `.env.example`.
5. Click **Create Web Service**.

---

### Option 2: Deploy to Railway

1. Install the Railway CLI or visit [railway.app](https://railway.app).
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository.
4. Railway will automatically detect the `Dockerfile` or `Procfile`.
5. Under the **Variables** tab, add your environment variables (`GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_DB_PASSWORD`, etc.).
6. Under **Settings** -> **Networking**, click **Generate Domain** to get your public API URL (e.g. `https://siksha-api.up.railway.app`).

---

### Option 3: Deploy to Fly.io

1. Install the [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/).
2. Login to your account:
   ```bash
   fly auth login
   ```
3. Launch the app using the included `fly.toml`:
   ```bash
   fly launch
   ```
4. Set your production secrets:
   ```bash
   fly secrets set GROQ_API_KEY="your-key" SUPABASE_DB_PASSWORD="your-db-password"
   ```
5. Deploy:
   ```bash
   fly deploy
   ```

---

### Option 4: Run with Docker Locally or on a VPS

1. Build the Docker image:
   ```bash
   docker build -t sikshasaathi-backend .
   ```
2. Run the container:
   ```bash
   docker run -d \
     -p 8000:8000 \
     --env-file .env \
     --name sikshasaathi-api \
     sikshasaathi-backend
   ```
3. Verify the container is running:
   ```bash
   docker ps
   curl http://localhost:8000/api/health
   ```

---

## 🩺 Health Check & Verification

Once deployed, verify your backend:

- **Health Check**: `GET https://your-backend-domain.com/api/health`
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-09-14T...",
    "database": "connected"
  }
  ```
- **API Documentation**: Open `https://your-backend-domain.com/docs` in your browser to inspect interactive OpenAPI documentation.
- **CORS Preflight Test**:
  ```bash
  curl -I -X OPTIONS https://your-backend-domain.com/api/auth/me \
    -H "Origin: https://sikshasaathi.vercel.app" \
    -H "Access-Control-Request-Method: GET"
  ```

# Zapchat CRM (FastAPI + Simple Frontend)
Minimal CRM for an auto parts store (avto zapchast) with FastAPI backend and a simple HTML+JS frontend.
- Backend: FastAPI, SQLAlchemy (works with PostgreSQL via DATABASE_URL env var; defaults to SQLite for local testing)
- Auth: Register / Login -> JWT tokens
- Entities: users, customers, parts, orders (basic)
- Deploy: Dockerfile included (suitable for Railway).

## Run locally (quick)
1. Create virtual env, install requirements:
   ```bash
   python -m venv venv; source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run (defaults to SQLite):
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Open frontend: `file://<repo>/app/static/index.html` or visit `http://localhost:8000/docs` for API docs.

## Railway / Production
- Railway sets DATABASE_URL env var for Postgres. Set SECRET_KEY as env var too.
- Dockerfile included; Railway will build image and use DATABASE_URL automatically.

## Files included
- app/: backend code
- Dockerfile, requirements.txt, docker-compose.yml (example)
- frontend: `app/static/index.html` simple UI using fetch and JWT token auth

Enjoy — agar xohlasangiz men loyihani Railway-ga deploy qilish bo‘yicha aniq bosqichma-bosqich ko‘rsatma ham beraman.

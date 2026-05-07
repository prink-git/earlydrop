
# EarlyDrop

A production-oriented platform for detecting student disengagement and managing instructor interventions.
---

## Overview

EarlyDrop uses engagement analytics and an explainable ML model to surface at‑risk students and provide a streamlined instructor workflow for interventions. It is built with a FastAPI backend, a Next.js dashboard, and Supabase (Postgres) data storage with RLS.

## Features

- Risk scoring (0–100) with Low/Medium/High tiers
- Explainable risk drivers per student
- 8‑week engagement timelines and aggregates
- Instructor intervention logging and history
- CSV seed generation (500 students, ~4K feature rows)
- Secure architecture: anon read / service-role write with Supabase RLS
- Fault-tolerant CSV fallback for offline demos

---

## Architecture

- Frontend (Next.js) — UI only talks to backend API
- Backend (FastAPI) — serves REST API, scoring, and write operations
- Database (Supabase Postgres) — `students`, `weekly_features`, `risk_scores`, `interventions`

Design notes:
- Dual-key access: `ANON_KEY` for reads, `SERVICE_ROLE_KEY` for server writes
- RLS enforces least-privilege for write operations
- CSV fallback keeps UI usable when DB is unavailable

---

## ML Pipeline

1. Data generation: deterministic CSV seed generator (`generate_csv.py`).
2. Feature engineering: temporal trends, engagement metrics, aggregates.
3. Model training: scikit‑learn pipeline (preprocessing + estimator). Store model artifacts externally.
4. Inference: batch precompute `risk_scores` for reads; per‑student explainability returned to UI.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Uvicorn, python-dotenv |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Data | Supabase (Postgres) |
| ML | scikit-learn, pandas, numpy |

---

## Repo layout

```
earlydrop/
├── backend/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── generate_csv.py
	├── data/
│   └── requirements.txt
├── frontend/
│   └── app/
├── migrations/
└── README.md
```

---

## API Endpoints

| Path | Method | Description |
|---:|:---:|---|
| `/health` | GET | Health check |
| `/students` | GET | Paginated student list (query: `limit`, `offset`, `q`) |
| `/students/{id}/timeline` | GET | Engagement & interventions |
| `/students/{id}/action` | POST | Log an intervention (server write) |

---

## Security & RLS

- Keep `SUPABASE_SERVICE_ROLE_KEY` out of the repo; use `.env` locally and platform secrets in CI/deploy.
- RLS: allow read for anon role; restrict `interventions` writes to service-role only.
- Audit fields on writes: `actor`, `created_at`, `note`.

---

## Local development

1. Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env    # fill locally
python main.py
```

2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Quick: `python generate_csv.py` to create seed CSVs in `backend/data/`.

---

## Deployment 

- Containerize backend; deploy to Railway/Render/GCP Cloud Run. Deploy frontend to Vercel.
- Store `SERVICE_ROLE_KEY` and other secrets in platform secret store. Enable Supabase backups and PITR for production.

---

## Scalability

- Precompute `risk_scores` for large cohorts; index `student_id` and time columns.
- Use pagination, caching for hot reads, and background workers for heavy jobs.

---

## Project Achievements 

- Built EarlyDrop: end-to-end ML product with FastAPI backend, Next.js UI, and Supabase RLS.
- Implemented reproducible seed and feature pipelines (500 students, 8-week timelines) and explainable scoring.
- Hardened deployment with dual-key access, server-only write policies, and CSV fallback for demo resilience.

---

## Future improvements

- Add model monitoring (drift detection) and scheduled retraining.
- Provide Docker Compose with a local Postgres option for full offline demos.
- Add role-based UI permissions and expanded audit logging.

---

## License

MIT — see `LICENSE`.

---

Last updated: May 8, 2026

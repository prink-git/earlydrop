# EarlyDrop 
### ML-Driven Student Dropout Risk Detection

EarlyDrop is an **end-to-end full-stack system** that detects **early student disengagement patterns** in online learning platforms using **unsupervised machine learning** and translates them into **actionable risk insights** for instructors.

---

## Problem Statement

Student dropouts in online education are typically **lagging indicators**, detected only after prolonged inactivity or failure.

EarlyDrop addresses this by:
- Monitoring **weekly behavioral engagement signals**
- Detecting **anomalous learning patterns** before hard dropouts
- Assigning **interpretable risk scores**
- Enabling **timely instructor intervention**

The system focuses on **early detection, not post-failure analysis**.

---

## Architecture
Next.js Frontend (Dashboard + Charts)  ->  FastAPI Backend (REST APIs)  ->  Supabase (PostgreSQL)  ->  ML Pipeline (Isolation Forest)

---

## Tech Stack

**Frontend**
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Recharts

**Backend**
- FastAPI
- Python 3.11
- Supabase Python SDK

**Machine Learning**
- scikit-learn
- Isolation Forest (unsupervised anomaly detection)

**Database**
- Supabase (PostgreSQL)
- Tables: students, events, weekly_features, risk_scores, interventions

#### Model: Isolation Forest
Reasoning:
- No labeled dropout data required
- Robust to noisy behavioral signals
- Risk scores derived from anomaly scores + domain thresholds
- Explanations generated from feature-level deviations
---
## Core Features
- Synthetic student activity simulation
- Weekly engagement feature engineering
- Unsupervised anomaly detection
- Continuous risk scoring (Low / Medium / High)
- Instructor dashboard with engagement trends, risk progression and intervention logging

---

## How to Run Locally
### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
### Frontend
```bash
cd frontend
npm install
npm run dev

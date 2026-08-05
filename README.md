# UDIAP — Universal Decision Intelligence Assessment Platform

**Measure How Humans Think, Decide and Adapt.**

AI-powered Decision Intelligence platform that analyzes not only user answers but the cognitive process behind decisions using:

- **Cognitive Observer Engine (COE)**
- **Human Decision Process Model (HDPM)**
- **Decision Genome** scoring

---

## Architecture

```
User → Next.js Frontend → FastAPI Backend → Services Layer → PostgreSQL
                              ↓
                    AI Engine (COE + HDPM + Scoring)
```

### Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | Next.js 14, React, TypeScript, Tailwind, Framer Motion, Recharts |
| Backend    | Python, FastAPI, SQLAlchemy (async), JWT |
| Database   | PostgreSQL                          |
| AI Engine  | Rule-based scoring (ML-ready), Scikit-learn architecture |

---

## Project Structure

```
udiap/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Config, security, database
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   └── seed.py
├── ai_engine/         # COE, HDPM, Scoring, Report Generator
├── database/
├── documentation/
└── tests/
```

---

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set DATABASE_URL in .env or use default
# Start PostgreSQL, then:
uvicorn app.main:app --reload --port 8000

# Seed sample data (in another terminal)
PYTHONPATH=. python seed.py
```

**Demo credentials after seed:**
- Admin: `admin@udiap.ai` / `Admin@12345`
- User:  `demo@udiap.ai`  / `Demo@12345`

### 2. Frontend

```bash
cd frontend
npm install
# optional: create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000/api
npm run dev
```

Open http://localhost:3000

### 3. API Docs

http://localhost:8000/docs

---

## Core Scoring Formula

```
FINAL SCORE = (Content Score × 0.60) + (Process Score × 0.40)
```

**Content dimensions:** Critical Thinking, Technical Reasoning, Risk Management, Communication  
**Process dimensions:** Decision Speed, Reflection, Adaptability, Revision Quality

---

## Pages

1. **Landing** — Hero, HDPM pipeline, COE explanation, feature cards  
2. **Dashboard** — DI Score, radar cognitive metrics, assessment list  
3. **Assessment Workspace** — Distraction-free editor + silent cognitive tracking  
4. **AI Report** — Score, radar, strengths/weaknesses, recommendations, HDPM analysis  
5. **Analytics** — Score trends, skill comparison  
6. **Admin** — User management, AI monitoring metrics  

---

## Security

- Password hashing (bcrypt)
- JWT access + refresh tokens
- Role-based access control (user / researcher / admin / superadmin)
- Input validation via Pydantic

---

## Future ML Integration

The scoring engine is deliberately modular. Feature extraction and prediction modules are ready for:

- Logistic Regression
- Random Forest
- Neural Networks (PyTorch)

Replace rule-based `ScoringEngine` methods with trained model inference without changing the API surface.

---

## License

Proprietary — UDIAP Research Platform

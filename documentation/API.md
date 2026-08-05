# UDIAP API Documentation

Base URL: `http://localhost:8000/api`

## Authentication

### POST /auth/register
```json
{ "name": "Jane", "email": "jane@ex.com", "password": "secret123" }
```

### POST /auth/login
```json
{ "email": "jane@ex.com", "password": "secret123" }
```
Returns: `access_token`, `refresh_token`, `user`

### GET /auth/me
Header: `Authorization: Bearer <token>`

## Assessments

### GET /assessments/
List active assessments

### GET /assessments/{id}
Full assessment with questions

### POST /assessments/start
```json
{ "assessment_id": 1 }
```
Returns `session_id` + assessment payload

### POST /assessments/submit
```json
{
  "session_id": "...",
  "question_id": 1,
  "answer_text": "...",
  "time_spent_seconds": 420,
  "word_count": 180
}
```

## Behaviour

### POST /behavior/log
Cognitive Observer events (keystrokes, pauses, revisions, etc.)

## Reports

### POST /report/generate
```json
{ "session_id": "..." }
```
Generates Decision Genome + AI Report

### GET /report/{id}
### GET /report/

## Analytics

### GET /analytics/dashboard
Score history, latest genome, totals

## Admin (role: admin | superadmin)

### GET /admin/users
### PATCH /admin/users/{id}
### POST /admin/assessments
### GET /admin/monitoring

# Student Manage API

FastAPI aur raw PostgreSQL (psycopg, bina ORM) se bana Student CRUD project.

## Tech Stack
- Python, FastAPI, Uvicorn
- PostgreSQL, psycopg
- python-dotenv

## Setup
1. Virtual environment banao: `python -m venv venv`
2. Activate karo: `venv\Scripts\activate`
3. Libraries lagao: `pip install -r requirements.txt`
4. `.env.example` ko copy karke `.env` banao aur apna PostgreSQL password daalo
5. PostgreSQL mein `student_db` database banao, phir `schema.sql` chalao
6. Server chalao: `uvicorn main:app --reload`

Docs page: http://127.0.0.1:8000/docs

## API Endpoints
| Method | URL | Kaam |
|--------|-----|------|
| POST | /students | Naya student add karo |
| GET | /students | Saare students dekho |
| GET | /students/{id} | Ek student dekho |
| PUT | /students/{id} | Poora student update karo |
| PATCH | /students/{id} | Sirf kuch fields update karo |
| DELETE | /students/{id} | Student delete karo |

## Validation
- Age 3 se 25 ke beech hi (API mein Pydantic Field, database mein CHECK constraint)
- Id na milne par 404 error
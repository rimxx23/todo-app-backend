# Todo App Backend

A REST API for managing tasks, built with FastAPI.
Each user can create and manage only their own tasks.

## Features

- User registration and login with JWT authentication
- Passwords are hashed with argon2
- Each user can see and edit only their own tasks
- Layered architecture: router → service → repository
- Async database access with SQLAlchemy
- Database migrations with Alembic
- 17 tests (unit and integration) on a separate test database
- Runs with one command using Docker Compose
- Simple web frontend (HTML + JavaScript, no build step)

## Tech stack

- Python, FastAPI
- PostgreSQL, SQLAlchemy (async), Alembic
- Pydantic, pydantic-settings
- JWT (PyJWT), pwdlib (argon2)
- Docker, Docker Compose
- pytest, pytest-asyncio, httpx

## API endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/auth/register` | Create a new user | — |
| POST | `/auth/login` | Get an access token | — |
| GET | `/auth/me` | Get the current user | ✅ |
| GET | `/tasks` | List your tasks | ✅ |
| POST | `/tasks` | Create a task | ✅ |
| PATCH | `/tasks/{task_id}` | Update a task | ✅ |
| DELETE | `/tasks/{task_id}` | Delete a task | ✅ |

Interactive documentation is available at http://localhost:8000/docs after the start.

## Getting started

1. Clone the repository and go to the project folder.

2. Create a `.env` file from the example and fill in your values:

   ```bash
   cp .env.example .env
   ```

   Generate a secret key for `SECRET_KEY`:

   ```bash
   openssl rand -hex 32
   ```

3. Start the app and the database:

   ```bash
   docker compose up --build
   ```

   Migrations are applied automatically on start.

4. Open http://localhost:8000/docs

5. (Optional) Start the frontend in a new terminal:

   ```bash
   python3 -m http.server 3001 --directory frontend
   ```

   Open http://localhost:3001 — use exactly this address,
   because CORS allows only the origins listed in `CORS_ALLOWED_ORIGIN`.

## Running tests

Tests use a separate database `todo_test`, so your data is not touched.

1. Create the test database (only once):

   ```bash
   docker compose exec db createdb -U <POSTGRES_USER> todo_test
   ```

2. Install dependencies and run the tests:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pytest -v
   ```

## Project structure

```text
todo-app-backend/
├── app/
│   ├── api/            # routers and dependencies
│   ├── core/           # settings and security (hashing, JWT)
│   ├── db/             # database session
│   ├── models/         # SQLAlchemy models
│   ├── repositories/   # database queries
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # business logic
│   └── main.py
├── alembic/            # database migrations
├── frontend/           # web interface (index.html)
├── tests/              # pytest tests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

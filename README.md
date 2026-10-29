# FastAPI Starter

Small FastAPI app with three sample APIs. Data is stored in memory and resets when the process stops.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- App: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

Copy `.env.example` to `.env` if you want to change the app name or CORS origins.

## Sample APIs

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/health` | Liveness check |
| GET | `/api/v1/items` | List items (`q`, `tag`, `skip`, `limit`) |
| POST | `/api/v1/items` | Create an item |
| GET | `/api/v1/items/{id}` | Fetch one item |
| PATCH | `/api/v1/items/{id}` | Update fields you send |
| DELETE | `/api/v1/items/{id}` | Delete an item |
| GET | `/api/v1/users` | List users (`role`, `skip`, `limit`) |
| POST | `/api/v1/users` | Create a user (email must be unique) |
| GET | `/api/v1/users/{id}` | Fetch one user |

Two items and two users are seeded on startup so the list endpoints return data immediately.

## Tests

```bash
pip install pytest
pytest
```

## Deploy on Vercel

Vercel runs this app as one Python function. It loads the `app` object from `app/main.py` (also set as `tool.vercel.entrypoint` in `pyproject.toml`) and installs the dependencies from `pyproject.toml`. The runtime is Python 3.12.

From this directory, with the [Vercel CLI](https://vercel.com/docs/cli):

```bash
npx vercel
```

Or push the repo and import it at [vercel.com/new](https://vercel.com/new). Leave the root directory as the repository root and let Vercel detect FastAPI. Do not set a custom Build Command.

Optional environment variables: `APP_NAME`, `DEBUG`, and `CORS_ORIGINS` (comma-separated origins).

Sample data is stored in memory inside the function. Each instance starts from the seed data, and creates, updates, and deletes are not shared across instances or kept after the instance stops.
# fastapistarter

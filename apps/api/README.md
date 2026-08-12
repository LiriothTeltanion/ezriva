# Ezriva API

The public API runtime still exposes only a typed FastAPI application and a
side-effect-free `GET /healthz` endpoint. The repository also contains the
isolated checklist-item-2 synthetic-fixture evaluation lab; it is not exposed
as an API route and normal startup does not initialize Strands or AWS.

Storage, uploads, authentication, and action tools have not been implemented.

Run from the repository root:

```bash
uv run uvicorn ezriva.main:app --app-dir apps/api/src --reload
```

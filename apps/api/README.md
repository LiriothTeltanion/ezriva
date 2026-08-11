# Ezriva API

The checklist-item-1 API contains only a typed FastAPI application and a
side-effect-free `GET /healthz` endpoint. It does not initialize Strands, AWS,
storage, uploads, authentication, or any action tool.

Run from the repository root:

```bash
uv run uvicorn ezriva.main:app --app-dir apps/api/src --reload
```

"""Health endpoint tests.

Module: test_health
Purpose: Verify the baseline API contract without external side effects.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

import asyncio

from httpx import ASGITransport, AsyncClient, Response

from ezriva.main import app


async def _request_health() -> Response:
    """Request health through ASGI without starting a network listener."""

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get("/healthz")


def test_health_endpoint_returns_exact_public_contract() -> None:
    """Health returns only status and version and never contacts a provider."""

    response = asyncio.run(_request_health())

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

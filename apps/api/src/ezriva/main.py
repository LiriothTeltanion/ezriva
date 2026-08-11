"""FastAPI application bootstrap for Ezriva.

Module: main
Purpose: Provide a side-effect-free API foundation and health contract.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from ezriva import __version__


class HealthResponse(BaseModel):
    """Public process-health response."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    version: str


def create_app() -> FastAPI:
    """Create the FastAPI application without contacting external services.

    Returns:
        Configured FastAPI application.
    """

    application = FastAPI(
        title="Ezriva API",
        version=__version__,
        description="Human-controlled document-to-action API foundation.",
    )

    @application.get("/healthz", response_model=HealthResponse, tags=["operations"])
    async def health() -> HealthResponse:
        """Return local process health without invoking a model or storage."""

        return HealthResponse(status="ok", version=__version__)

    return application


app = create_app()

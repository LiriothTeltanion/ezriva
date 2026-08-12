"""Bounded Hebrew document-understanding spike for checklist item 2.

Module: ai_spike
Purpose: Export extraction-only schemas and deterministic evaluation gates.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from ezriva.ai_spike.gate import GateDecision, GateDisposition, evaluate_candidate
from ezriva.ai_spike.schemas import DocumentBriefCandidate

__all__ = [
    "DocumentBriefCandidate",
    "GateDecision",
    "GateDisposition",
    "evaluate_candidate",
]

"""Versioned record constructors and validation."""

from __future__ import annotations

from typing import Any

from .errors import StateError


RUN_SCHEMA = "run-manifest/v1"
EVIDENCE_SCHEMA = "evidence-packet/v1"
APPROVAL_SCHEMA = "approval-receipt/v1"
VERIFICATION_SCHEMA = "verification-receipt/v1"
TRANSFER_SCHEMA = "transfer-receipt/v1"
COMPLETION_SCHEMA = "completion-receipt/v1"

TERMINAL_STATUSES = {"cancelled", "completed", "dry_run", "failed"}

ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "preparing": {"planning", "dry_run", "cancelled", "failed"},
    "planning": {"synthesizing", "cancelled", "failed"},
    "synthesizing": {"adversarial", "cancelled", "failed"},
    "adversarial": {"finalizing", "cancelled", "failed"},
    "finalizing": {"awaiting_approval", "cancelled", "failed"},
    "awaiting_approval": {"approved", "cancelled", "failed"},
    "approved": {"implementing", "cancelled", "failed"},
    "implementing": {"implemented", "cancelled", "failed"},
    "implemented": {"reviewing", "cancelled", "failed"},
    "reviewing": {"reviewed", "review_failed", "cancelled", "failed"},
    "review_failed": {"reviewing", "cancelled", "failed"},
    "reviewed": {"verifying", "cancelled", "failed"},
    "verifying": {"verified", "cancelled", "failed"},
    "verified": {"completing", "cancelled", "failed"},
    "completing": {"completed", "failed"},
}


def require_fields(record: dict[str, Any], fields: tuple[str, ...], schema: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise StateError(f"{schema} missing required fields: {', '.join(missing)}")


def validate_manifest(record: dict[str, Any]) -> None:
    require_fields(
        record,
        ("schema", "run_id", "status", "created_at", "updated_at", "repository", "models", "artifacts", "attempts"),
        RUN_SCHEMA,
    )
    if record["schema"] != RUN_SCHEMA:
        raise StateError(f"unsupported manifest schema: {record['schema']!r}")
    if not isinstance(record["repository"], dict) or not isinstance(record["models"], dict):
        raise StateError("manifest repository/models fields must be objects")
    if not isinstance(record["artifacts"], dict) or not isinstance(record["attempts"], list):
        raise StateError("manifest artifacts/attempts fields have invalid types")


def transition(record: dict[str, Any], status: str, *, now: str) -> None:
    validate_manifest(record)
    current = str(record["status"])
    if status == current:
        return
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    if status not in allowed:
        raise StateError(f"invalid state transition: {current} -> {status}")
    record["status"] = status
    record["updated_at"] = now


def validate_evidence(record: dict[str, Any]) -> None:
    require_fields(record, ("schema", "run_id", "created_at", "request", "repository", "constraints", "environment"), EVIDENCE_SCHEMA)
    if record["schema"] != EVIDENCE_SCHEMA:
        raise StateError(f"unsupported evidence schema: {record['schema']!r}")


def validate_approval(record: dict[str, Any]) -> None:
    require_fields(
        record,
        ("schema", "run_id", "approved_at", "method", "plan_sha256", "repository_sha", "evidence_sha256"),
        APPROVAL_SCHEMA,
    )
    if record["schema"] != APPROVAL_SCHEMA:
        raise StateError(f"unsupported approval schema: {record['schema']!r}")


def validate_verification(record: dict[str, Any]) -> None:
    require_fields(
        record,
        ("schema", "run_id", "verified_at", "success", "commands", "diff_sha256", "approval_sha256"),
        VERIFICATION_SCHEMA,
    )
    if record["schema"] != VERIFICATION_SCHEMA:
        raise StateError(f"unsupported verification schema: {record['schema']!r}")

"""Controller-specific failures with stable exit-code semantics."""

from __future__ import annotations


class CrosscheckError(RuntimeError):
    """Base class for expected, user-facing controller failures."""

    exit_code = 1


class UsageError(CrosscheckError):
    exit_code = 2


class StateError(CrosscheckError):
    exit_code = 3


class SafetyError(CrosscheckError):
    exit_code = 4


class ProviderError(CrosscheckError):
    exit_code = 5

    def __init__(self, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.retryable = retryable


class CancelledError(CrosscheckError):
    exit_code = 130

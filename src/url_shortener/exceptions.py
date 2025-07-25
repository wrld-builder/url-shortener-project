"""
Custom exception types for the URL shortener application.

Defining specific exception classes allows the rest of the codebase to catch
and handle error conditions in a meaningful way.  Higher‑level layers can
translate these exceptions into appropriate HTTP responses or user‑facing
messages without leaking implementation details.
"""


class ShortURLNotFoundError(Exception):
    """Raised when a short code cannot be resolved to an original URL."""


class URLAlreadyExistsError(Exception):
    """Raised when attempting to shorten a URL that already exists in the system."""


class InvalidURLError(Exception):
    """Raised when a supplied URL fails validation."""

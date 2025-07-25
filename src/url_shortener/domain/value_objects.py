"""
Value objects used in the domain layer.

A value object represents a concept with identity defined entirely by its
attributes rather than a distinct identity.  In this simple URL shortener
domain we define a ``URL`` class that validates and normalises the
user‑supplied input.  This class is immutable and comparable by value to
support equality checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse, urlunparse


@dataclass(frozen=True)
class URL:
    """Immutable value object representing an absolute URL.

    A ``URL`` performs basic validation and normalisation on the provided
    string.  It enforces a scheme (``http`` or ``https``) and requires a
    network location (host).  The resulting normalised form is stored as
    ``value``.  Should validation fail, a ``ValueError`` is raised.
    """

    value: str

    def __post_init__(self) -> None:
        parsed = urlparse(self.value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {self.value}")
        if parsed.scheme not in ("http", "https"):
            raise ValueError(
                f"Unsupported scheme '{parsed.scheme}'. Only 'http' and 'https' are allowed."
            )
        # normalise: remove default port, ensure lower‑case scheme and host
        normalised = parsed._replace(scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower())
        object.__setattr__(self, "value", urlunparse(normalised))

    def __str__(self) -> str:
        return self.value

"""
Domain layer for the URL shortener.

This module exposes the core domain objects and value objects used by the
application.  These classes encapsulate business rules and invariants but do
not depend on any persistence or framework code.  They form the heart of
the system and should remain free of side effects to facilitate testing and
reuse.
"""

from .models import ShortURL  # noqa: F401
from .value_objects import URL  # noqa: F401

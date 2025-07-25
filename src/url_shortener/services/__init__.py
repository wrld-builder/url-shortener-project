"""
Service layer for the URL shortener.

Services orchestrate operations between the domain and repository layers.
They encapsulate application logic, manage transactions, and coordinate
multiple domain objects.  The service layer exposes a public API to the
interfaces (such as web controllers or command‑line clients) and hides
lower‑level details like code generation and persistence concerns.
"""

from .shortener_service import ShortenerService  # noqa: F401
from .code_generator import AbstractCodeGenerator, RandomCodeGenerator  # noqa: F401

"""
Repository interfaces and implementations.

The repository layer abstracts away the details of how entities are
persisted and retrieved.  By programming against an interface rather than a
concrete implementation, the domain and service layers can remain agnostic
to whether data lives in memory, a relational database, or a remote
key–value store.  This flexibility facilitates unit testing and allows
infrastructure concerns to change independently of business logic.
"""

from .repository_interface import AbstractShortURLRepository  # noqa: F401
from .in_memory_repository import InMemoryShortURLRepository  # noqa: F401

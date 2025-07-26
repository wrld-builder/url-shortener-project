"""
In‑memory repository implementation for ``ShortURL`` entities.

This repository stores entities in a simple Python dictionary.  It uses a
singleton pattern to ensure that only one instance exists within the
application.  The in‑memory repository is suitable for development,
testing, or scenarios where persistence across restarts is not required.
"""

from __future__ import annotations

from threading import Lock
from typing import Dict, Optional

from .repository_interface import AbstractShortURLRepository
from ..domain.models import ShortURL


class InMemoryShortURLRepository(AbstractShortURLRepository):
    """Concrete in‑memory implementation of the repository interface."""

    _instance: Optional["InMemoryShortURLRepository"] = None
    _lock: Lock = Lock()

    def __new__(cls) -> "InMemoryShortURLRepository":  # pragma: no cover
        """Ensure a single instance (singleton) across the application."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # initialise storage on the singleton instance
                    cls._instance._storage: Dict[str, ShortURL] = {}
                    cls._instance._url_index: Dict[str, ShortURL] = {}
                    cls._instance._id_counter: int = 1
        return cls._instance

    def next_id(self) -> int:
        """Return the next unique identifier and increment the counter."""
        current = self._id_counter
        self._id_counter += 1
        return current

    def add(self, short_url: ShortURL) -> None:
        """Add or update a ``ShortURL`` in the repository.

        This method indexes the entity by both its ``short_code`` and its
        ``original_url`` for fast lookups on subsequent operations.
        """
        self._storage[short_url.short_code] = short_url
        self._url_index[short_url.original_url] = short_url

    def clear(self) -> None:
        """Очистить все записи (для удобства запуска тестов)."""

        self._storage.clear()

    def get_by_code(self, code: str) -> Optional[ShortURL]:
        return self._storage.get(code)

    def get_by_original(self, url: str) -> Optional[ShortURL]:
        return self._url_index.get(url)

"""
Abstract repository interfaces.

This module defines the contracts that concrete repository implementations
must fulfil.  Repositories encapsulate all persistence logic and provide
methods for adding and retrieving domain entities.  A repository is a
collection–like object that acts as a bridge between the domain and
infrastructure layers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from ..domain.models import ShortURL


class AbstractShortURLRepository(ABC):
    """Abstract base class for short URL repositories."""

    @abstractmethod
    def next_id(self) -> int:
        """Generate or fetch the next unique identifier for a new ``ShortURL``.

        Repositories are responsible for allocating IDs when new entities are
        created.  In a database implementation this might correspond to
        auto‑incrementing primary keys.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, short_url: ShortURL) -> None:
        """Persist a new ``ShortURL`` entity.

        Args:
            short_url: The entity to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[ShortURL]:
        """Retrieve a ``ShortURL`` entity by its code.

        Args:
            code: The unique short code.

        Returns:
            The corresponding ``ShortURL`` entity or ``None`` if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_original(self, url: str) -> Optional[ShortURL]:
        """Retrieve a ``ShortURL`` entity by its original URL.

        Args:
            url: The original, full URL.

        Returns:
            The corresponding ``ShortURL`` entity or ``None`` if not found.
        """
        raise NotImplementedError

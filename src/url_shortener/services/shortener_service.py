"""
Application service for shortening and resolving URLs.

This class coordinates between the domain objects, repositories and code
generator to provide a simple API for creating and retrieving shortened
links.  It also enforces certain business rules, such as avoiding
duplicate entries and handling collisions when generating codes.  Higher
layers (like web controllers) interact with this service instead of
directly manipulating repositories or domain objects.
"""

from __future__ import annotations

from ..domain.models import ShortURL
from ..domain.value_objects import URL
from ..exceptions import URLAlreadyShortenedError, InvalidURLError
from ..repositories import AbstractShortURLRepository
from .code_generator import AbstractCodeGenerator


class ShortenerService:
    """Service orchestrating URL shortening and resolution."""

    def __init__(
        self, repository: AbstractShortURLRepository, code_generator: AbstractCodeGenerator
    ) -> None:
        self._repository = repository
        self._code_generator = code_generator

    def shorten_url(self, url: str) -> ShortURL:
        """Create or retrieve a ``ShortURL`` for the given URL.

        Args:
            url: The original URL string supplied by the user.

        Returns:
            A ``ShortURL`` entity representing the shortened link.

        Raises:
            InvalidURLError: If the URL fails validation.
            URLAlreadyExistsError: If a mapping for this URL already exists.
        """
        try:
            url_vo = URL(url)
        except ValueError as exc:
            raise InvalidURLError(str(exc)) from exc

        # Check if URL already shortened
        existing = self._repository.get_by_original(str(url_vo))
        if existing:
            # To emphasise immutability of URL value objects we return the existing entity
            raise URLAlreadyShortenedError(
                f"The URL '{url_vo}' has already been shortened with code '{existing.short_code}'."
            )

        # Generate a unique code; avoid collisions by regenerating if necessary
        code = self._generate_unique_code()
        entity_id = self._repository.next_id()
        short_url = ShortURL(
            id=entity_id,
            original_url=str(url_vo),
            short_code=code,
        )
        self._repository.add(short_url)
        return short_url

    def resolve_url(self, code: str) -> ShortURL:
        """Retrieve the ``ShortURL`` entity corresponding to the given code.

        Args:
            code: The short code provided by the client.

        Returns:
            The ``ShortURL`` entity.

        Raises:
            ShortURLNotFoundError: If no mapping exists for the provided code.
        """
        entity = self._repository.get_by_code(code)
        if not entity:
            raise URLAlreadyShortenedError(f"No URL mapping found for code '{code}'")
        # business rule: update hit count on each access
        entity.increment_hits()
        return entity

    def _generate_unique_code(self) -> str:
        """Generate a code and ensure it is unique in the repository."""
        while True:
            code = self._code_generator.generate()
            if self._repository.get_by_code(code) is None:
                return code

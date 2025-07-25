"""
Code generator implementations.

Generating unique short codes is a distinct concern from both persistence and
business logic.  Abstracting this behaviour behind an interface makes it
possible to swap in different strategies (random, sequential, hashing) or
even delegate to external services without impacting the rest of the codebase.
"""

from __future__ import annotations

import os
import random
import string
from abc import ABC, abstractmethod
from typing import Iterable


class AbstractCodeGenerator(ABC):
    """Interface for code generator strategies."""

    @abstractmethod
    def generate(self) -> str:
        """Return a new unique short code."""
        raise NotImplementedError


class RandomCodeGenerator(AbstractCodeGenerator):
    """Generate short codes using a cryptographically strong random source.

    By default this generator produces alphanumeric codes of a fixed length
    using ``os.urandom`` for randomness.  The length is configurable and
    should be chosen based on expected cardinality and collision tolerance.
    """

    _characters: Iterable[str] = string.ascii_letters + string.digits

    def __init__(self, length: int = 6) -> None:
        if length <= 0:
            raise ValueError("length must be positive")
        self.length = length

    def generate(self) -> str:
        # ``os.urandom`` provides cryptographic randomness; we convert bytes
        # into indices to select characters from our allowed set.  This avoids
        # biases that can occur when using ``random.choice`` repeatedly.
        result_chars = []
        while len(result_chars) < self.length:
            random_bytes = os.urandom(self.length)
            for b in random_bytes:
                idx = b % len(self._characters)
                result_chars.append(self._characters[idx])
                if len(result_chars) == self.length:
                    break
        return "".join(result_chars)

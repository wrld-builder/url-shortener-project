"""
Base62 encoding and decoding utilities.

Base62 encodes binary or integer values into a compact string representation
using digits, uppercase and lowercase letters.  It is commonly used for
generating short, human‑friendly identifiers.  These functions can be used
to convert database primary keys into a short code or vice versa.

Note: The functions below operate on non‑negative integers.  Negative values
will raise a ``ValueError``.
"""

from __future__ import annotations

import string
from typing import Dict


ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
BASE = len(ALPHABET)
CHAR_TO_VALUE: Dict[str, int] = {ch: idx for idx, ch in enumerate(ALPHABET)}


def encode_base62(number: int) -> str:
    """Encode a non‑negative integer into a base62 string.

    Args:
        number: The integer to encode.

    Returns:
        A base62 representation of ``number``.

    Raises:
        ValueError: If ``number`` is negative.
    """
    if number < 0:
        raise ValueError("number must be non‑negative")
    if number == 0:
        return ALPHABET[0]
    result = []
    while number > 0:
        number, remainder = divmod(number, BASE)
        result.append(ALPHABET[remainder])
    return "".join(reversed(result))


def decode_base62(s: str) -> int:
    """Decode a base62 string back into an integer.

    Args:
        s: The base62 string to decode.

    Returns:
        The decoded integer value.

    Raises:
        ValueError: If the string contains characters outside the Base62 alphabet.
    """
    result = 0
    for ch in s:
        if ch not in CHAR_TO_VALUE:
            raise ValueError(f"Invalid base62 character: '{ch}'")
        result = result * BASE + CHAR_TO_VALUE[ch]
    return result

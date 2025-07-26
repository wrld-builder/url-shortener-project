# src/url_shortener/utils/base62.py
"""
Base62 encoding and decoding utilities.
"""
import string

_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase

def encode_base62(num: int) -> str:
    if num < 0:
        raise ValueError("Cannot encode negative numbers")
    if num == 0:
        return _alphabet[0]
    parts = []
    base = len(_alphabet)
    while num:
        num, rem = divmod(num, base)
        parts.append(_alphabet[rem])
    return ''.join(reversed(parts))

def decode_base62(s: str) -> int:
    if not s:
        raise ValueError("Cannot decode empty string")
    base = len(_alphabet)
    num = 0
    for char in s:
        num = num * base + _alphabet.index(char)
    return num

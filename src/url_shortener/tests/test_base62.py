import pytest
from url_shortener.utils.base62 import encode_base62, decode_base62

@pytest.mark.parametrize("num,expected", [
    (0, "0"),
    (61, "z"),
    (62, "10"),
    (3843, "zz"),
])
def test_base62_roundtrip(num, expected):
    code = encode_base62(num)
    assert code == expected
    assert decode_base62(code) == num

import pytest
from url_shortener.services.shortener_service import ShortenerService
from url_shortener.services.code_generator import RandomCodeGenerator
from url_shortener.repositories.in_memory_repository import InMemoryShortURLRepository
from url_shortener.exceptions import URLAlreadyShortenedError

@pytest.fixture
def service():
    repo = InMemoryShortURLRepository()
    repo.clear()
    return ShortenerService(repo, RandomCodeGenerator())

def test_shorten_and_resolve(service):
    record = service.shorten_url("https://openai.com")
    assert record.original_url == "https://openai.com"
    resolved = service.resolve_url(record.short_code)
    assert resolved.original_url == "https://openai.com"
    assert resolved.hits == 1

def test_duplicate_shortening(service):
    with pytest.raises(URLAlreadyShortenedError):
        service.shorten_url("https://openai.com")

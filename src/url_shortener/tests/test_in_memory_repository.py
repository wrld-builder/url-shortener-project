from url_shortener.domain.models import ShortURL
from url_shortener.repositories.in_memory_repository import InMemoryShortURLRepository

def test_repo_add_and_get():
    repo = InMemoryShortURLRepository()
    repo.clear()  # очищаем между тестами
    model = ShortURL(original_url="https://example.com", short_code="abc123")
    repo.add(model)
    fetched = repo.get_by_code("abc123")
    assert fetched == model

def test_repo_nonexistent():
    repo = InMemoryShortURLRepository()
    repo.clear()
    assert repo.get_by_code("nope") is None

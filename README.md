# URL Shortener Project

This repository contains a simple yet **carefully architected** URL shortener
service written in pure Python.  While the underlying functionality is
straight‑forward—mapping long URLs to short codes and resolving them back—the
project is designed to showcase several software design patterns and clean
architecture principles.  The emphasis is on separation of concerns,
maintainability and extensibility rather than brevity.

## Architecture Overview

The codebase is organised into distinct layers inspired by
**Domain‑Driven Design (DDD)** and the **Clean Architecture** philosophy:

| Layer        | Responsibility                                                     |
|--------------|--------------------------------------------------------------------|
| **Domain**   | Contains the core business entities (`ShortURL`) and immutable value objects (`URL`). These classes encapsulate business rules without depending on any external libraries or persistence concerns. |
| **Repositories** | Provide interfaces (`AbstractShortURLRepository`) and implementations (e.g., `InMemoryShortURLRepository`) for persisting entities. The rest of the system depends only on the interface, allowing the storage mechanism to vary. |
| **Services** | Coordinate operations between the domain and repositories. The `ShortenerService` orchestrates the creation and resolution of short links. The `RandomCodeGenerator` encapsulates the strategy for generating unique codes. |
| **Utilities** | House generic helpers such as Base62 encoding, which are independent of the business logic. |
| **Application (Interfaces)** | Expose the service layer to the outside world. In this project, `app/main.py` implements a minimal HTTP API using Python’s `http.server` module. |

The following design patterns and principles are intentionally demonstrated:

* **Singleton Pattern** – `InMemoryShortURLRepository` ensures that a single repository instance is shared across the application, preventing inconsistent state between requests.
* **Repository Pattern** – Abstracts away persistence details and provides a collection‑like interface to the domain.  This decouples the rest of the system from the choice of storage (in‑memory, SQLite, etc.).
* **Factory/Strategy Pattern** – `AbstractCodeGenerator` defines a contract for generating short codes, and `RandomCodeGenerator` is one concrete strategy.  New strategies (e.g., sequential, hash‑based) can be added without modifying existing code.
* **Value Object** – The `URL` class enforces validation and normalisation rules and is immutable.  Value objects are compared by value rather than identity.
* **Service Layer** – `ShortenerService` encapsulates application logic, enforcing business rules such as avoiding duplicate URLs and updating hit counts.
* **Separation of Concerns** – Each layer has a single responsibility and depends only on the layer below it, making the system easier to test and evolve.

## Running the Server

The project is dependency‑free and uses only the Python standard library.  To
start the HTTP server locally, execute the following commands:

```bash
cd src/url_shortener/app
python3 main.py
```

By default the server listens on port `8000`.  Once running you can use
`curl` or any HTTP client to interact with it:

* **Shorten a URL:**

  ```bash
  curl -X POST http://localhost:8000/shorten \
       -H 'Content-Type: application/json' \
       -d '{"url": "https://example.com"}'
  ```

  The response will be a JSON object containing the short code and the full
  short URL.

* **Resolve a short code:**

  ```bash
  curl -v http://localhost:8000/<code>
  ```

  This request will return a 302 redirect to the original URL, or a 404
  JSON response if the code does not exist.

## Extensibility

The current implementation uses an in‑memory repository and a random code
generator.  Replacing these components is straightforward:

* **Persistent Storage:** Implement a new class that inherits from
  `AbstractShortURLRepository` (e.g., `SQLiteShortURLRepository`) and
  registers it with the service.  This would allow links to persist across
  restarts.
* **Alternative Code Generation Strategies:** Create a new class that
  implements `AbstractCodeGenerator` (e.g., `SequentialCodeGenerator` using
  Base62 encoding of database IDs).  Inject this new generator into
  `ShortenerService` to change how codes are produced.

Because of the clear boundaries and adherence to interfaces, adding such
features does not require changes to the domain or service layers.

## Testing

You can write unit tests in the `tests/` directory using your favourite test
framework (e.g., `unittest` or `pytest`).  Since the core logic is
decoupled from the HTTP layer, testing the service and repository is
straight‑forward.  For example:

```python
from url_shortener.services import ShortenerService, RandomCodeGenerator
from url_shortener.repositories import InMemoryShortURLRepository

def test_shorten_and_resolve():
    repo = InMemoryShortURLRepository()
    service = ShortenerService(repo, RandomCodeGenerator())
    short = service.shorten_url("https://example.com")
    assert short.original_url == "https://example.com"
    resolved = service.resolve_url(short.short_code)
    assert resolved.original_url == "https://example.com"
    assert resolved.hits == 1
```

## Conclusion

Although the functionality provided by this project is simple, the emphasis
on **strong design and architecture** demonstrates how even trivial
applications can benefit from clear boundaries and patterns.  This approach
lays the groundwork for more complex features while keeping the codebase
maintainable and understandable.

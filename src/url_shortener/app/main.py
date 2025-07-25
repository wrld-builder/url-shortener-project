"""
Minimal HTTP interface for the URL shortener.

This module defines a simple HTTP server using Python's standard library.
It implements two endpoints:

* ``POST /shorten`` – Accepts a JSON payload containing a URL to shorten and
  returns a JSON response with the generated code and fully qualified short
  URL.  If the URL is invalid or already exists, it returns an error message
  with the appropriate HTTP status code.
* ``GET /<code>`` – Redirects clients to the original URL associated with
  ``<code>``.  If no mapping exists, it returns a 404 response with a JSON
  error payload.

Because the standard library's HTTP server lacks many conveniences found in
frameworks like Flask or FastAPI, the request parsing and response
construction logic is somewhat verbose.  However, using only built‑in
modules keeps the project free of external dependencies and makes it
portable to restricted environments.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Tuple

from ..config import BASE_HOST, DEFAULT_CODE_LENGTH
from ..exceptions import InvalidURLError, ShortURLNotFoundError, URLAlreadyExistsError
from ..repositories import InMemoryShortURLRepository
from ..services import RandomCodeGenerator, ShortenerService


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    """Helper to send a JSON response with the given status and payload."""
    response_body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(response_body)))
    handler.end_headers()
    handler.wfile.write(response_body)


class ShortenerRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler implementing the shortener API."""

    # Instantiate service with singleton repository and code generator
    _repository = InMemoryShortURLRepository()
    _code_generator = RandomCodeGenerator(length=DEFAULT_CODE_LENGTH)
    _service = ShortenerService(_repository, _code_generator)

    def do_POST(self) -> None:  # noqa: N802  (method names must override base class)
        """Handle POST requests for creating a new shortened URL."""
        if self.path.rstrip("/") != "/shorten":
            self.send_error(404, "Not Found")
            return

        # Read and parse JSON body
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)
        try:
            body = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
        except json.JSONDecodeError:
            _json_response(self, 400, {"error": "Invalid JSON body"})
            return

        url = body.get("url")
        if not url:
            _json_response(self, 400, {"error": "Missing 'url' in request body"})
            return

        try:
            short_entity = self._service.shorten_url(url)
        except InvalidURLError as exc:
            _json_response(self, 400, {"error": str(exc)})
            return
        except URLAlreadyExistsError as exc:
            # Conflict when URL already exists
            _json_response(self, 409, {"error": str(exc)})
            return

        # Build absolute short URL using the host header if available
        host = self.headers.get("Host") or BASE_HOST.strip("/")
        short_url = f"http://{host}/{short_entity.short_code}"
        payload = {
            "code": short_entity.short_code,
            "short_url": short_url,
            "original_url": short_entity.original_url,
        }
        _json_response(self, 201, payload)

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests for resolving a short code."""
        # Remove leading slash and any query string
        code = self.path.lstrip("/").split("?")[0]
        if not code:
            # root path provides a simple landing page
            body = {
                "message": "URL Shortener Service",
                "instructions": {
                    "shorten": "Send POST /shorten with JSON {'url': 'https://example.com'}",
                    "redirect": "Navigate to /<code> to be redirected",
                },
            }
            _json_response(self, 200, body)
            return

        try:
            entity = self._service.resolve_url(code)
        except ShortURLNotFoundError as exc:
            _json_response(self, 404, {"error": str(exc)})
            return
        # On success, redirect to the original URL
        self.send_response(302)
        self.send_header("Location", entity.original_url)
        self.end_headers()


def run_server(address: Tuple[str, int] = ("", 8000)) -> None:
    """Run the HTTP server until interrupted."""
    server = HTTPServer(address, ShortenerRequestHandler)
    host, port = server.server_address
    print(f"Serving on {host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()

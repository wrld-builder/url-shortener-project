"""
Application configuration settings.

Centralising configuration in this module allows the rest of the codebase to
read configuration values from a single location.  In a more sophisticated
application you might load these values from environment variables or a
configuration file.  For this simple example we expose a base URL and the
default length of generated short codes.
"""

# Base URL used when constructing fully qualified short URLs.  In a
# production deployment this would correspond to the domain of the service.
BASE_HOST = "http://localhost:8000"

# Default length for generated short codes.  See ``RandomCodeGenerator`` for
# details on how this value influences uniqueness and collision rates.
DEFAULT_CODE_LENGTH = 6

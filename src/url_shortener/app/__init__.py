"""
Entry points and user interfaces for the URL shortener.

The ``app`` package contains modules that expose the functionality of the
application layer to the outside world.  This could take the form of a
command‑line interface, a RESTful HTTP API, a graphical user interface, or
any other delivery mechanism.  Keeping these interfaces in a dedicated
package ensures that the core service and domain logic remain decoupled
from the specifics of input/output handling.
"""

from .main import run_server  # noqa: F401

"""Core module exposes the document interfaces
These will be ingested via Drones, built by Builders, and served via the API.
"""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("emmet-api")
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass

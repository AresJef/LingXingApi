import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

from lingxingapi.api import API
from lingxingapi import errors

__all__ = [
    "API",
    "errors",
]

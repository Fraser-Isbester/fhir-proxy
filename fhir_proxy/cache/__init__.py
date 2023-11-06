"""Contains caching logic for the application."""

from fhir_proxy.cache.redis_cache import (
    caches,
    get_redis,
    invalidates,
)

__all__ = [
    "caches",
    "invalidates",
    "get_redis"
]

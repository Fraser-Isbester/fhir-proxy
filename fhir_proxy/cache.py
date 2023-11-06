"""Contains caching logic for the application."""

import json
from functools import wraps

import redis.asyncio as aioredis
from fastapi import HTTPException
from redis.exceptions import RedisError

from fhir_proxy import config


async def get_redis() -> aioredis.Redis:
    try:
        redis = aioredis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)
        await redis.ping()
        return redis
    except RedisError:
        return None

def cache(key_pattern: str, expiration: int = 5):
    """Manages a basic caching approach for a function."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            # Builds a cache key from the key pattern and the function arguments
            cache_key = key_pattern.format(*args, **kwargs)

            # Fetch the redis instance from the function arguments
            redis = kwargs.get('redis', await get_redis())

            if redis:
                try:
                    # Attempt to get cached response
                    cached_response = await redis.get(cache_key)
                    if cached_response:
                        return json.loads(cached_response)
                except RedisError:
                    print(f"Failed to read from Redis for key: {cache_key}")

            # If there is no cached response, call the wrapped function
            response = await func(*args, **kwargs)

            if redis:
                try:
                    # Attempt to cache the response
                    await redis.set(cache_key, json.dumps(response), ex=expiration)
                except RedisError:
                    print(f"Failed to cache response for key: {cache_key}")

            return response
        return wrapper
    return decorator

async def invalidate_cache(redis: aioredis.Redis, key: str):
    try:
        await redis.delete(key)
        print(f"Cache invalidated for key: {key}")
    except RedisError:
        print(f"Failed to invalidate cache for key: {key}")


def invalidates(key_pattern: str, fail_on_error: bool = False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the function first
            response = await func(*args, **kwargs)

            # Determine the Redis key for this request
            cache_key = key_pattern.format(*args, **kwargs)
            redis = kwargs.get('redis', await cache())

            if redis:
                # Invalidate the cache
                try:
                    await invalidate_cache(redis, cache_key)
                except RedisError as e:
                    if fail_on_error:
                        raise HTTPException(status_code=500, detail="Failed to invalidate cache.") from e
                    else:
                        print(f"Cache invalidation failed for key: {cache_key}, error: {e}")

            return response
        return wrapper
    return decorator


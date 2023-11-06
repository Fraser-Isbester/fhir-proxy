import json
from unittest.mock import AsyncMock

import pytest
from redis import Redis
from redis.exceptions import RedisError

from fhir_proxy.cache import cache, get_redis, invalidate_cache, invalidates

# Use pytest-asyncio for async test functions
pytestmark = pytest.mark.asyncio

async def test_get_redis_success(mocker):
    # Mock redis.from_url to return a mock Redis client
    mock_redis = AsyncMock(Redis)
    mocker.patch('redis.asyncio.from_url', return_value=mock_redis)

    # Mock the ping method to simulate a successful connection
    mock_redis.ping = AsyncMock()

    redis = await get_redis()

    # Assert that the redis instance was successfully retrieved
    assert redis is mock_redis

async def test_get_redis_failure(mocker):
    # Mock redis.asyncio.from_url to raise RedisError
    mocker.patch('redis.asyncio.from_url', side_effect=RedisError)

    redis = await get_redis()

    # Assert that None is returned when RedisError is raised
    assert redis is None

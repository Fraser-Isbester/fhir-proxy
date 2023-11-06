import time

import httpx
from fastapi import Depends, FastAPI, HTTPException
from redis import Redis

from fhir_proxy.cache import cache, get_redis, invalidates

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/healthcheck-cache")
async def healthcheck_cache(redis: Redis = Depends(get_redis)):
    redis.ping()
    return {"status": "ok"}


@app.get("/")
async def read_resource():
    return "Hello, world!"

@app.get("/beers/{typ}")
@cache(key_pattern="beers:{typ}")
async def get_beers(typ: str, redis: Redis = Depends(get_redis)):
    try:
        r = httpx.get(f"https://api.sampleapis.com/beers/{typ}")
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

@app.put("/beers/{typ}")
@invalidates(key_pattern="beers:{typ}")
async def set_beers(typ: str, data: dict, redis: Redis = Depends(cache)):
    # simulate network delay
    time.sleep(.2)
    return {"status": "success", "message": "Beers updated and cache invalidated"}

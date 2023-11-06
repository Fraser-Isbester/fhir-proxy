import time

import httpx
from fastapi import Depends, FastAPI, HTTPException
from redis import Redis

from fhir_proxy import cache
from fhir_proxy.routers import fhir_api

app = FastAPI()

# Registers the FHIR API router with the application
app.include_router(fhir_api.router, prefix="/api/v1", tags=["FHIR API"])

@app.get("/")
async def read_resource():
    return {"status", "ok"}

@app.get("/beers/{typ}")
@cache.caches(key_pattern="beers:{typ}")
async def get_beers(typ: str, redis: Redis = Depends(cache.get_redis)):
    try:
        r = httpx.get(f"https://api.sampleapis.com/beers/{typ}")
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

@app.put("/beers/{typ}")
@cache.invalidates(key_pattern="beers:{typ}")
async def set_beers(typ: str, data: dict, redis: Redis = Depends(cache.get_redis)):
    # simulate network delay
    time.sleep(.2)
    return {"status": "success", "message": "Beers updated and cache invalidated"}

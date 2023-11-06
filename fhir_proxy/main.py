import time

import httpx
from fastapi import Depends, FastAPI, HTTPException
from redis import Redis

from fhir_proxy import cache
from fhir_proxy.routers import fhir_api

app = FastAPI()

@app.get("/")
async def read_resource():
    return {"status", "ok"}

# Registers the FHIR API router with the application
app.include_router(fhir_api.router, prefix="/api/v1", tags=["FHIR API"])
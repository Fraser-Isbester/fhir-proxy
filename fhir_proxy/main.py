import time

from fastapi import FastAPI, Request

from fhir_proxy.routers import simple

app = FastAPI()


@app.get("/")
async def read_resource():
    return {"status", "ok"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Registers the FHIR API router with the application
app.include_router(simple.router, prefix="/api/v1", tags=["FHIR API"])

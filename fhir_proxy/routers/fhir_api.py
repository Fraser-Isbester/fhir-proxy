from fastapi import APIRouter

from fhir_proxy import cache

router = APIRouter()

@router.post("/fhir/{resource_type}/")
@cache.invalidates(key_pattern="{resource_type}:{id}")
async def create_resource(resource_type: str):
    """Create a new FHIR resource of a specified type."""
    return {
        "resourceType": resource_type,
        "id": "abc123"
    }

@router.get("/fhir/{resource_type}/{id}")
@cache.caches(key_pattern="{resource_type}:{id}")
async def get_resource(resource_type: str, id: str):
    """Read a FHIR resource by type and ID."""

    return {
        "resourceType": resource_type,
        "id": id,
    }

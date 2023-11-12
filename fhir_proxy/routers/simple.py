from fastapi import APIRouter, Body
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient

import fhir_proxy.types.simple as simple

router = APIRouter()

@router.post("/simple/person/", response_model=Patient)
async def create_person(person: simple.Person = Body(...)):
    """Create a new FHIR Patient resource from a simple person object."""
    # patient = mapping.r4.patient.from_person(person)
    patient = Patient(
        name=[
            HumanName(family=person.last_name, given=[person.first_name])
        ],
        birthDate=person.date_of_birth
    )

    print(patient.json(indent=2))


    # Return the Patient resource
    return patient


# @router.post("/simple/{resource_type}/")
# @cache.invalidates(key_pattern="{resource_type}:{id}")
# async def create_resource(resource_type: str):
#     """Create a new FHIR resource of a specified type."""
#     return {"resourceType": resource_type, "id": "abc123"}


# @router.get("/simple/{resource_type}/{id}")
# @cache.caches(key_pattern="{resource_type}:{id}")
# async def get_resource(resource_type: str, id: str, response: Response):
#     """Read a FHIR resource by type and ID."""

#     return {"resourceType": resource_type, "id": id}
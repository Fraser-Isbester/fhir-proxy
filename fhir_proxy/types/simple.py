from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

__all__ = [
    "CreatePersonRequest",
    "CreatePersonResponse",
    "Person",
]

class CreatePersonRequest(BaseModel):
    """Person creation request body."""
    person: "Person"

class CreatePersonResponse(BaseModel):
    """Person creation request body."""
    person: "Person"

class Person(BaseModel):
    """Person model."""
    id: Optional[str] = Field(None, example="550e8400-e29b-41d4-a716-446655440000")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    date_of_birth: date = Field(..., example="1980-01-01")
    gender: Optional[str] = Field(None, example="male")

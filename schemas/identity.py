import datetime
from typing import Optional

from pydantic import BaseModel, Field

from models.identity import SEXE_CHOICES, STATUS_CHOICES


class IdentityBaseSchema(BaseModel):
    first_name: str
    birth_date: datetime.date
    birth_place: str
    address: str
    sexe: SEXE_CHOICES


class CreateIdentitySchema(IdentityBaseSchema):
    last_name: Optional[str] = Field(None)
    distinctive_trait: Optional[str] = Field(None)
    profession: Optional[str] = Field(None)
    father_id: Optional[int] = Field(None)
    mother_id: Optional[int] = Field(None)


class IdentitySchema(CreateIdentitySchema):
    id: int
    identity_key: str
    status: STATUS_CHOICES

    class Config:
        from_attributes = True

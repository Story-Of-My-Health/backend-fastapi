import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from models.identity import SEXE_CHOICES, STATUS_CHOICES

class UserSchema(BaseModel):
    id: int
    user_type: str

class IdentityMedicalHistorySchema(BaseModel):
    id: int
    created_by: int
    symptoms: str
    treatment: str


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
    medical_history: List[IdentityMedicalHistorySchema]
    profile_img: Optional[str] = Field(None)
    user: Optional[UserSchema] = Field(None)
    class Config:
        from_attributes = True


class IdentityQuerySchema(BaseModel):
    first_name: Optional[str] = None
    address: Optional[str] = None
    sexe: Optional[SEXE_CHOICES] = None
    status: Optional[STATUS_CHOICES] = None


class UpdateIdentitySchema(BaseModel):
    first_name: str
    last_name: Optional[str]
    address: str
    distinctive_trait: Optional[str]
    profession: Optional[str]
    father_id: Optional[int]
    mother_id: Optional[int]

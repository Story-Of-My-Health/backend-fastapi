from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from schemas.identity import IdentitySchema


class MedicalHistoryBaseSchema(BaseModel):
    symptoms: str
    treatment: str


class CreateMedicalHistory(MedicalHistoryBaseSchema):
    patient_id: int


class MedicalHistorySchema(MedicalHistoryBaseSchema):
    id: int
    created_by: int
    patient_id: int


class KeywordSchema(BaseModel):
    id: int
    name: str


class DoctorProfileBaseSchema(BaseModel):
    title: str
    establishment: str
    address: str


class CreateDoctorProfileSchema(DoctorProfileBaseSchema):
    keywords: List[str]


class DoctorProfileSchema(DoctorProfileBaseSchema):
    id: int
    keywords: List[KeywordSchema]


class UserBaseSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class CreateUserSchema(UserBaseSchema):
    identity_id: int
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    user_type: str
    identity: IdentitySchema
    doctor_profile: Optional[DoctorProfileSchema] = None

    # class Config:
    #     from_attributes = True


class DecodedToken(UserBaseSchema):
    id: int
    user_type: str
    identity_id: int

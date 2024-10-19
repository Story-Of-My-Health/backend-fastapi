from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from schemas.identity import IdentitySchema


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

    class Config:
        from_attributes = True


class DecodedToken(UserBaseSchema):
    id: int
    user_type: str
    identity_id: int

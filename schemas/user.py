from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class CreateUserSchema(UserBaseSchema):
    identity_key: str
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str

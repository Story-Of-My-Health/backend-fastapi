from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str
    password: str

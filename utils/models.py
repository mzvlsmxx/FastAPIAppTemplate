from enum import Enum
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Bearer token")


class TokenData(BaseModel):
    user_id: int | None = Field(default=None, description="Subject (username) from JWT")


class SignUpResults(Enum):
    success = "Registration succeed"
    already_exists = "User already exists"
    fail = "Registration failed"


class SignUpResult(BaseModel):
    result: SignUpResults = Field(default=SignUpResults.fail, description="User")


class UserBase(BaseModel):
    username: str = Field(default="", description="Username")
    first_name: str = Field(default="", max_length=100, description="First name")
    middle_name: str = Field(default="", max_length=100, description="Middle name")
    last_name: str = Field(default="", max_length=100, description="Last name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=5, description="Plain password")
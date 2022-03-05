from typing import Optional
from pydantic import BaseModel


class SignupData(BaseModel):

    username: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "g4st0n",
                "email": "mail@gastonotero.com",
                "password": "lionelmessi123"
            }
        }


class SigninData(BaseModel):

    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "mail@gastonotero.com",
                "password": "lionelmessi123"
            }
        }


class SignupSigninReturn(BaseModel):
    user_id: str
    jwt: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "1",
                "jwt": "eyJ0eXAiOiJKV1Qi...",
            }
        }


class UserData(BaseModel):
    email: str
    username: str
    conversation_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "email": "mail@gastonotero.com",
                "username": "g4st0n",
                "conversation_id": 4
            }
        }

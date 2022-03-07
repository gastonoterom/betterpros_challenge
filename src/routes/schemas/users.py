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
    user_id: int
    jwt: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": "1",
                "jwt": "eyJ0eXAiOiJKV1Qi...",
            }
        }


class UserDataReturn(BaseModel):
    email: str
    username: str
    conversation_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "email": "peer@mail.com",
                "username": "peer_142",
                "conversation_id": 45
            }
        }

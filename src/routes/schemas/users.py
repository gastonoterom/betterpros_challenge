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

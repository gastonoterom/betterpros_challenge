from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.crud.users import get_user_by_id
from src.database.session_factory import session_factory
from src.libs.crypto import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def auth_required(token: str = Depends(oauth2_scheme),
                        session: Session = Depends(session_factory)):
    """Auth middleware for protected routes, throws an 401 error if bearer token is not present or
    invalid, if not, it returns the User object related to the token's user id"""

    token_data = decode_jwt(token)

    if token_data is None:
        raise HTTPException(
            status_code=401, detail="error: invalid token")

    return get_user_by_id(token_data.get("user_id"), session)

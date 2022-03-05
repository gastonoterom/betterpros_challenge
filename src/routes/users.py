from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.database.crud.conversations import get_p2p_conversation
from src.database.crud.users import get_user_by_email, get_user_by_id, insert_user, user_exists
from src.database.session_factory import session_factory
from src.database.models import User
from src.routes.auth.token_middleware import auth_required
from src.routes.schemas.users import SigninData, SignupData
from src.libs.crypto import hash_text, generate_jwt, validate_hash

router = APIRouter()


@router.post("/signup")
async def signup(signup_data: SignupData, session: Session = Depends(session_factory)):

    user = User(email=signup_data.email,
                username=signup_data.username, hashed_pass=hash_text(signup_data.password))

    if user_exists(user, session):
        raise HTTPException(
            status_code=409, detail="username/email already registered")

    insert_user(user, session)

    return {"user_id": user.id, "jwt": generate_jwt(user.id)}


@router.post("/login")
async def login(signin_data: SigninData, session: Session = Depends(session_factory)):

    user: User = get_user_by_email(signin_data.email, session)

    if user is None or not validate_hash(signin_data.password, user.hashed_pass):
        raise HTTPException(
            status_code=401, detail="error: invalid username or password")

    return {"user_id": user.id, "jwt": generate_jwt(user.id)}


@router.get("/user/{user_id}")
async def get_user(
        user_id: int,
        user: User = Depends(auth_required),
        session: Session = Depends(session_factory)):

    if user_id == user.id:
        return {"email": user.email, "username": user.username}

    peer = get_user_by_id(user_id, session)

    if peer is None:
        raise HTTPException(
            status_code=404, detail="User not found")

    response = {
        "email": user.email,
        "username": user.username,
    }

    if convo_in_common := get_p2p_conversation(user.id, peer.id, session):
        response["conversation_id"] = convo_in_common.id

    return response

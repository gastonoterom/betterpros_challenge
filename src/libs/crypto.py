from secrets import token_urlsafe
from typing import Optional
import bcrypt
import jwt

# For testing purposes a cryptographically safe secret is generated randomly on the go,
# in production this should be an env variable, or even better, it should use
# public-key cryptography

TOKEN_SECRET = token_urlsafe(40)
ALGORITHM = "HS256"


def hash_text(text: str) -> str:
    """Hashes a given utf-8 string with the bcrypt algorithm."""
    return bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")


def validate_hash(text: str, hashed_text: str) -> bool:
    """Returns True if the hash of a text match (both in utf-8), False if not"""
    return bcrypt.checkpw(text.encode('utf-8'), hashed_text.encode('utf-8'))


def generate_jwt(user_id: int):
    """Generates an access token for a user"""
    return jwt.encode({"user_id": user_id}, TOKEN_SECRET, algorithm=ALGORITHM)


def decode_jwt(token: str) -> Optional[dict]:
    """Validates and decodes a jwt, returns None if jwt could not be decoded"""

    try:
        return jwt.decode(token, TOKEN_SECRET, algorithms=[ALGORITHM])

    except jwt.exceptions.DecodeError:
        return None

from secrets import token_urlsafe
from typing import Optional
import bcrypt
import jwt

# For testing purposes a cryptographically safe secret is generated randomly on the go,
# in production this should be an env variable, or even better, it should use
# public-key cryptography

TOKEN_SECRET = token_urlsafe(40)

def get_token():
    return TOKEN_SECRET

def hash_text(text: str) -> str:
    """Hashes a given utf-8 string with the bcrypt algorithm."""
    return bcrypt.hashpw(text.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")


def validate_hash(text: str, hashed_text: str) -> bool:
    """Returns True if the hash of a text match (both in utf-8), False if not"""
    return bcrypt.checkpw(text.encode('utf-8'), hashed_text.encode('utf-8'))


def generate_jwt(user_id: int, token_secret: str):
    """Generates an access token for a user"""
    return jwt.encode({"user_id": user_id}, token_secret, algorithm="HS256")


def decode_jwt(token: str, token_secret: str) -> Optional[dict]:
    """Validates and decodes a jwt, returns None if jwt could not be decoded"""

    try:
        return jwt.decode(token, token_secret, algorithms=["HS256"])

    except jwt.exceptions.DecodeError:
        return None

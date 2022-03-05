from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from src.database.models import User


def user_exists(user: User, session: Session) -> bool:
    """Verifies if a user is registered in the database (by email)

    Returns True if they are, False if not"""

    return get_user_by_email(user.email, session) is not None


def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
    """Gets a desired user by id, returns None if no user is found"""
    return session.query(User).filter_by(id=user_id).first()


def get_user_by_email(email: str, session: Session) -> Optional[User]:
    """Gets a desired user by their email, returns None if no user is found"""
    return session.query(User).filter_by(email=email).first()


def insert_user(user: User, session: Session) -> None:
    """Inserts a modeled user into the database, returns the insertion id"""

    session.add(user)
    session.commit()

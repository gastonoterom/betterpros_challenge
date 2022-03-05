from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Conversation,  UserAndConversation


def p2p_convo_exists(id_1: int, id_2: int, session: Session) -> bool:
    """Returns True if a p2p conversation between two users exists, by id"""
    return get_p2p_conversation(id_1, id_2, session) is not None


def get_p2p_conversation(id_1: int, id_2: int, session: Session) -> Optional[Conversation]:
    """Get a p2p conversation between two users by id, returns None if not found

    Raises ValueError if both ids are the same"""
    if id_1 == id_2:
        raise ValueError("Peer ids can't be the same")

    return session.query(Conversation).filter(Conversation.users.any(user_id=id_1)) \
        .filter(Conversation.users.any(user_id=id_2)).filter_by(type=0).first()


def insert_conversation(conv: Conversation, members_id: List[int], session: Session) -> None:
    """Insert a conversation into the db with their respective members"""
    for member_id in members_id:
        conv.users.append(UserAndConversation(user_id=member_id))

    session.add(conv)
    session.commit()


def is_conversation_member(user_id: int, conversation_id: int, session: Session) -> bool:
    """Validates if a certain user is a member of a certain conversation"""
    return session.query(Conversation).filter(Conversation.users.any(user_id=user_id)).\
        filter_by(id=conversation_id).first() is not None


def get_conversation_by_id(conversation_id: int, session: Session) -> Optional[Conversation]:
    """Returns a conversation by it's id, or None if not found"""
    return session.query(Conversation).filter_by(id=conversation_id).first()

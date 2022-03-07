from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.database.crud.conversations import get_conversation_by_id, insert_conversation, \
    is_conversation_member, p2p_convo_exists
from src.database.models import Conversation, User
from src.database.session_factory import session_factory
from src.routes.auth.token_middleware import auth_required
from src.routes.schemas.conversations import ConversationData, ConversationsResponse, \
    ConversationResponse

router = APIRouter()


#####################
# Create conversation

# Middlewares

async def parse_conversation(conversation_data: ConversationData):
    """Parse the conversation data into a conversation object"""
    return Conversation(title=conversation_data.title, type=conversation_data.type)


async def handle_convo_members(conversation_data: ConversationData,
                               user: User = Depends(auth_required)):
    """Returns a conversation members list, from the request body and the user id from the
    authorization token"""

    guests, user_id = conversation_data.guests, user.id

    # To avoid conversation owner id duplication:
    return [*guests, user_id] if user_id not in guests else guests


async def validate_conversation(
        conversation: Conversation = Depends(parse_conversation),
        members: List[int] = Depends(handle_convo_members),
        session: Session = Depends(session_factory)):

    """Validate the business rules of p2p convos: only 2 users, only 1 convo per pair"""

    if conversation.type == 0:
        if len(members) != 2:
            raise HTTPException(
                status_code=400, detail="error: p2p rooms only allow 2 participants")

        if p2p_convo_exists(*members, session):
            raise HTTPException(
                status_code=409, detail="error: p2p room for both users already exists")

    return conversation

# Route


@router.post("/conversations", response_model=ConversationsResponse)
async def post_conversations(
        conversation: Conversation = Depends(validate_conversation),
        members: List[int] = Depends(
            handle_convo_members),
        session: Session = Depends(session_factory)) -> ConversationsResponse:

    """Route for creating p2p or group conversations"""

    insert_conversation(conversation, members, session)

    return ConversationsResponse(conversation_id=conversation.id)


#####################
# Get conversation

# Middlewares

async def authorize_conversation_info(
        conversation_id: int,
        user: User = Depends(auth_required),
        session: Session = Depends(session_factory)):

    conversation = get_conversation_by_id(conversation_id, session)

    if conversation is None:
        raise HTTPException(
            status_code=404, detail="conversation does not exist")

    if not is_conversation_member(user.id, conversation.id, session):
        raise HTTPException(
            status_code=401, detail="unauthorized: requester is not allowed in room")

    return conversation

# Route


@router.get("/conversation/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
        conversation: Conversation = Depends(authorize_conversation_info)) -> ConversationResponse:
    """Route to fetch a conversation's info, only for conversation participants"""

    return ConversationResponse(id=conversation.id,
                                title=conversation.title,
                                type="p2p" if
                                conversation.type == Conversation.ConversationType.P2P else "group",
                                members=list(map(lambda user: user.user_id, conversation.users)))

from typing import List, Optional
from pydantic import BaseModel, Field


class ConversationData(BaseModel):
    """Conversation data for database storage.

    conversation types have to be 0 or 1"""

    title: Optional[str]
    type: int = Field(ge=0, le=1)
    guests: List[int]

    class Config:
        schema_extra = {
            "example": {
                "title": "2022 Qatar world cup bets",
                "type": 1,
                "guests": [5, 12, 56, 75, 24]
            }
        }


class ConversationsResponse(BaseModel):

    conversation_id: int

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": 1,
            }
        }


class ConversationResponse(BaseModel):

    id: int
    title: Optional[str]
    type: str
    members: List[int]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "group room",
                "type": "group",
                "members": [2, 6, 23]
            }
        }

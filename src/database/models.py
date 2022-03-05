from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.db_engine import Base, engine


def create_tables(db_engine=engine):
    """Create the modeled tables in the database, testing only"""
    Base.metadata.create_all(bind=db_engine)


class UserAndConversation(Base):
    """ORM representation of the many-to-many relationships between users and their
    conversations"""

    __tablename__ = 'user_conversation'

    # Columns
    user_id = Column(ForeignKey('user_account.id'), primary_key=True)
    conversation_id = Column(ForeignKey('conversation.id'), primary_key=True)

    # Relations
    conversation = relationship("Conversation", back_populates="users")
    user = relationship("User", back_populates="conversations")


class Conversation(Base):
    """ORM representation of a p2p or group conversation in the database"""

    __tablename__ = 'conversation'

    # Columns
    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(Integer)  # 0 = p2p, 1 = group

    # Relations
    users = relationship("UserAndConversation",
                         back_populates="conversation")

    def __repr__(self):
        return f"(Conversation id={self.id},title={self.title},type={self.type})"


class User(Base):
    """ORM representation of a user account in the database"""

    __tablename__ = 'user_account'

    # Columns
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    hashed_pass = Column(String)

    # Relations
    conversations = relationship("UserAndConversation", back_populates="user")

    def __repr__(self):
        return f"(User id={self.id},email={self.email},username={self.username})"

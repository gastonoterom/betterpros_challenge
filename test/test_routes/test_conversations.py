from unittest import IsolatedAsyncioTestCase
from test.mocks.database import get_mock_session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.crud.conversations import insert_conversation
from src.routes.conversations import authorize_conversation_info, get_conversation, \
    handle_convo_members, parse_conversation, post_conversations, validate_conversation
from src.routes.schemas.conversations import ConversationData
from src.database.crud.users import insert_user
from src.database.models import Conversation, User, UserAndConversation
from src.libs.crypto import hash_text


class TestUsers(IsolatedAsyncioTestCase):

    def setUp(self):

        self.session: Session = get_mock_session()

        insert_user(User(id=1, username="g4st0n", email="mail@gastonotero.com",
                    hashed_pass=hash_text("password")), self.session)

        insert_user(User(id=2, username="marina", email="marina@mail.com",
                    hashed_pass=hash_text("password2")), self.session)

        insert_user(User(id=3, username="beto", email="beto@mail.com",
                    hashed_pass=hash_text("password3")), self.session)

        insert_conversation(Conversation(
            id=1, type=0, title="secret chat"), [1, 2], self.session)
        insert_conversation(Conversation(id=2, type=1, title="group chat"), [
                            1, 2, 3], self.session)

        self.token_secret = "test"

    async def test_parse_conversation(self):

        conversation = await parse_conversation(
            ConversationData(title="testing", type=1, guests=[1, 2]))

        self.assertTrue(isinstance(conversation, Conversation))

    async def test_handle_convo_members(self):

        # conversation owner: 1, guests: 2 & 3

        conv_data = ConversationData(title="testing", type=1, guests=[2, 3])
        user = User(id=1)
        members = await handle_convo_members(conv_data, user)

        self.assertTrue(len(members) == 3)
        self.assertTrue(1 in members and 2 in members and 3 in members)

        # conversation owner: 1, guests: 1 & 2

        conv_data = ConversationData(title="testing", type=1, guests=[1, 2])
        user = User(id=1)
        members = await handle_convo_members(conv_data, user)

        self.assertTrue(len(members) == 2)
        self.assertTrue(1 in members and 2 in members)

    async def test_validate_conversation(self):
        # Valid p2p conversation: 2 members & no previous conversation
        conversation = Conversation(type=0, title="valid p2p")
        members = [1, 3]

        validated_conversation = await validate_conversation(
            conversation, members, self.session)

        self.assertIsNotNone(validated_conversation)

        # Valid group conversation
        group_conversation = Conversation(type=1, title="valid group")
        members = [1, 2, 3]

        validated_group_conversation = await validate_conversation(
            group_conversation, members, self.session)

        self.assertIsNotNone(validated_group_conversation)

        # Invalid p2p conversation: 2 members & previous conversation
        duplicate_conversation = Conversation(type=0, title="duplicate p2p")
        members = [2, 1]

        with self.assertRaises(HTTPException):
            await validate_conversation(duplicate_conversation, members, self.session)

        # Invalid p2p conversation: more than 2 members
        big_conversation = Conversation(type=0, title="big p2p")
        members = [2, 1, 3]

        with self.assertRaises(HTTPException):
            await validate_conversation(big_conversation, members, self.session)

    async def test_post_conversations(self):
        conversation_data = await post_conversations(Conversation(type=0), [1, 3], self.session)
        self.assertTrue(conversation_data["conversation_id"] == 3)

    async def test_authorize_conversation_info(self):
        # Test non existant conversation
        with self.assertRaises(HTTPException):
            await authorize_conversation_info(100, User(id=1), self.session)

        # Test trying to enter non authorized conversation
        with self.assertRaises(HTTPException):
            await authorize_conversation_info(1, User(id=3), self.session)

        conversation = await authorize_conversation_info(1, User(id=1), self.session)

        self.assertTrue(conversation.id == 1)

    async def test_get_conversation(self):

        conversation = Conversation(
            id=1, title="test", type=0, users=[UserAndConversation(user_id=1),
                                               UserAndConversation(user_id=2)])

        conversation_data = await get_conversation(conversation)

        self.assertEqual(conversation_data["id"], 1)
        self.assertEqual(conversation_data["title"], "test")
        self.assertEqual(conversation_data["type"], "p2p")
        self.assertEqual(len(conversation_data["members"]), 2)

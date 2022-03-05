import unittest
from test.mocks.database import get_mock_session
from sqlalchemy.orm import Session
from src.database.crud.users import insert_user
from src.database.models import Conversation, User
from src.database.crud.conversations import get_conversation_by_id, get_p2p_conversation, \
    insert_conversation, is_conversation_member, p2p_convo_exists


class TestConversationsCRUD(unittest.TestCase):

    def setUp(self):
        self.session: Session = get_mock_session()

        insert_user(User(id=1, email="mail@mail.com",
                    username="mail", hashed_pass="hash"), self.session)

        insert_user(User(id=2, email="mail2@mail.com",
                    username="mail2", hashed_pass="hash2"), self.session)
        insert_user(User(id=3, email="mail3@mail.com",
                    username="mail3", hashed_pass="hash3"), self.session)

    def test_conversations_crud(self):
        # Inserting a conversation
        conversation = Conversation(type=0, title="p2p convo")
        insert_conversation(conversation, [1, 2], self.session)

        # Get existant conversation by id
        conversation_1 = get_conversation_by_id(1, self.session)

        self.assertIsNotNone(conversation_1)
        self.assertEqual(conversation_1.id, 1)
        self.assertEqual(conversation_1.title, "p2p convo")
        self.assertEqual(conversation_1.type, 0)

        # Get a non existant conversation by id
        conversation_100 = get_conversation_by_id(100, self.session)

        self.assertIsNone(conversation_100)

        # Get p2p conversation that exists
        conversation_p2p = get_p2p_conversation(1, 2, self.session)

        self.assertIsNotNone(conversation_p2p)
        self.assertEqual(conversation_p2p.id, 1)

        # Error: trying to get a p2p convo from the user to itself
        with self.assertRaises(ValueError):
            get_p2p_conversation(1, 1, self.session)

        # Test if a p2p conv between two users exists
        self.assertTrue(p2p_convo_exists(1, 2, self.session))
        self.assertFalse(p2p_convo_exists(1, 3, self.session))

        # Test if a user is a member of a certain conversation
        self.assertTrue(is_conversation_member(1, 1, self.session))
        self.assertFalse(is_conversation_member(3, 1, self.session))

        # Inserting two group conversation with the same users is allowed
        conversation_1 = Conversation(type=1, title="group convo 1")
        conversation_2 = Conversation(type=1, title="group convo 2")

        insert_conversation(conversation_1, [1, 2, 3], self.session)
        insert_conversation(conversation_2, [1, 2, 3], self.session)

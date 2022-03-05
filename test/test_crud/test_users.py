import unittest
from test.mocks.database import get_mock_session
from sqlalchemy.orm import Session
from src.database.crud.users import get_user_by_email, get_user_by_id, insert_user, user_exists
from src.database.models import User


class TestUsersCRUD(unittest.TestCase):

    def setUp(self):
        self.session: Session = get_mock_session()

    def test_users_crud(self):
        # Inserting a user
        insert_user(User(id=1, email="mail@mail.com",
                    username="mail", hashed_pass="hash"), self.session)

        # Fetching an existing user by id
        user_1 = get_user_by_id(1, self.session)

        self.assertIsNotNone(user_1)
        self.assertEqual(user_1.id, 1)
        self.assertEqual(user_1.email, "mail@mail.com")
        self.assertEqual(user_1.username, "mail")
        self.assertEqual(user_1.hashed_pass, "hash")

        # Fetching a non-existant user by id
        user_100 = get_user_by_id(100, self.session)

        self.assertEqual(user_100, None)

        # Fetching an existing user by email
        user_mail = get_user_by_email("mail@mail.com", self.session)

        self.assertIsNotNone(user_mail)
        self.assertEqual(user_mail.id, 1)
        self.assertEqual(user_mail.email, "mail@mail.com")
        self.assertEqual(user_mail.username, "mail")
        self.assertEqual(user_mail.hashed_pass, "hash")

        # Fetching a non-existant user by email
        user_badmail = get_user_by_email("badmail@mail.com", self.session)

        self.assertEqual(user_badmail, None)

        # Checking if existing user exists
        self.assertTrue(user_exists("mail@mail.com", self.session))

        # Checking if non existing user exists
        self.assertFalse(user_exists("badmail@mail.com", self.session))

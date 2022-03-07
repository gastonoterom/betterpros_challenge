from unittest import IsolatedAsyncioTestCase
from src.database.crud.conversations import insert_conversation
from test.mocks.database import get_mock_session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.crud.users import insert_user
from src.database.models import Conversation, User
from src.libs.crypto import decode_jwt, hash_text
from src.routes.schemas.users import SigninData, SignupData
from src.routes.users import get_user, login, signup


class TestUsers(IsolatedAsyncioTestCase):

    def setUp(self):
        self.session: Session = get_mock_session()

        insert_user(User(username="g4st0n", email="mail@gastonotero.com",
                    hashed_pass=hash_text("password")), self.session)

        insert_user(User(username="marina", email="marina@mail.com",
                    hashed_pass=hash_text("password2")), self.session)

        self.token_secret = "test"

    async def test_signup(self):

        # Good signup
        signup_data = SignupData(
            email="beto@mail.com", username="el_beto", password="beto123")
        signup_response = await signup(signup_data, self.session, self.token_secret)

        self.assertEqual(signup_response.user_id, 3)

        self.assertIsNotNone(signup_response.jwt)
        self.assertIsNotNone(
            decode_jwt(signup_response.jwt, self.token_secret))

        # Bad signup: email already taken
        bad_signup_data = SignupData(
            email="beto@mail.com", username="batman", password="joker123")

        with self.assertRaises(HTTPException):
            await signup(bad_signup_data, self.session, self.token_secret)

    async def test_signin(self):
        # Good signin
        login_data = SigninData(
            email="mail@gastonotero.com", password="password")
        login_response = await login(login_data, self.session, self.token_secret)

        self.assertEqual(login_response.user_id, 1)
        self.assertIsNotNone(login_response.jwt)
        self.assertIsNotNone(decode_jwt(
            login_response.jwt, self.token_secret))

        # Bad signin: bad email
        bad_email = SigninData(
            email="xxxxx@gastonotero.com", password="password")

        with self.assertRaises(HTTPException):
            await login(bad_email, self.session, self.token_secret)

        # Bad signin: bad password
        bad_pass = SigninData(
            email="mail@gastonotero.com", password="xxxxxx")

        with self.assertRaises(HTTPException):
            await login(bad_pass, self.session, self.token_secret)

    async def test_get_user(self):
        myself = User(id=1, email="mail@gastonotero.com", username="g4st0n")

        # user requests their data
        my_data = await get_user(1, myself, self.session)

        self.assertEqual(my_data.email, "mail@gastonotero.com")
        self.assertEqual(my_data.username, "g4st0n")

        # user requests the data of a peer (no conv shared)
        peer_data = await get_user(2, myself, self.session)

        self.assertEqual(peer_data.email, "marina@mail.com")
        self.assertEqual(peer_data.username, "marina")
        self.assertEqual(peer_data.conversation_id, None)

        # user requests the data of a peer (conv shared)
        insert_conversation(Conversation(type=0), [1, 2], self.session)

        peer_data_2 = await get_user(2, myself, self.session)

        self.assertEqual(peer_data_2.email, "marina@mail.com")
        self.assertEqual(peer_data_2.username, "marina")
        self.assertEqual(peer_data_2.conversation_id, 1)

        # user requests data of a non existant peer
        with self.assertRaises(HTTPException):
            await get_user(100, myself, self.session)

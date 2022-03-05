from unittest import IsolatedAsyncioTestCase
from test.mocks.database import get_mock_session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.crud.users import insert_user
from src.database.models import User
from src.libs import crypto
from src.libs.crypto import hash_text
from src.routes.auth.token_middleware import auth_required


class TestTokenMiddleware(IsolatedAsyncioTestCase):

    def setUp(self):
        self.session: Session = get_mock_session()

        insert_user(User(username="g4st0n", email="mail@gastonotero.com",
                    hashed_pass=hash_text("password")), self.session)

    async def test_auth(self):
        user_id, test_secret = 1, "test secret"

        # Happy path
        token = crypto.generate_jwt(user_id, test_secret)
        user = await auth_required(token, self.session, test_secret)
        self.assertEqual(user.id, user_id)

        # Bad token
        bad_token = crypto.generate_jwt(user_id, "bad secret!")
        with self.assertRaises(HTTPException):
            await auth_required(bad_token, self.session, test_secret)

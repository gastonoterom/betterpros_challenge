import unittest
import src.libs.crypto as crypto


class TestCrypto(unittest.TestCase):

    def test_hash(self):
        test_string = "I'mAVerySecure_pass@2d!!!#"
        hashed_string = crypto.hash_text(test_string)

        self.assertTrue(crypto.validate_hash(test_string, hashed_string))
        self.assertFalse(crypto.validate_hash(
            "this should be false...", hashed_string))

    def test_jwt(self):
        token_secret = "PulpF!ct!0n31!^@$#6"
        user_id = 100

        token = crypto.generate_jwt(user_id, token_secret)
        bad_token = crypto.generate_jwt(user_id, "bad_secret")

        token_data = crypto.decode_jwt(token, token_secret)
        bad_token_data = crypto.decode_jwt(bad_token, token_secret)

        self.assertIsNotNone(token_data)
        self.assertIsNone(bad_token_data)

        self.assertEqual(token_data["user_id"], user_id)

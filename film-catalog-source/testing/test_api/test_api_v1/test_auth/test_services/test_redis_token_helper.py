from os import getenv
from unittest import TestCase

from api.api_v1.auth.services import redis_tokens

if getenv("TESTING") != "1":
    message = "Environment is not ready for testing"
    raise OSError(message)


class RedisTokenHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token(nbytes=10)
        self.assertTrue(
            redis_tokens.token_exists(new_token),
        )

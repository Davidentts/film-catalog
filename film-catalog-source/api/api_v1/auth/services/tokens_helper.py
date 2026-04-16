from abc import ABC, abstractmethod
import secrets


class AbstractTokensHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if token exists
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str):
        """
        Save token to storage
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls, nbytes: int = 32) -> str:
        return secrets.token_urlsafe(nbytes=nbytes)

    def generate_and_save_token(self, nbytes: int = 32) -> str:
        token = self.generate_token(nbytes)
        self.add_token(token)
        return token

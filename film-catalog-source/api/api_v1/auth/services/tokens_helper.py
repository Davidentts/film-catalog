import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelper(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if token exists
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Save token to storage
        :param token:
        :return:
        """

    @abstractmethod
    def delete_token(self, token: str) -> bool:
        """
        Delete token from storage
        :param token:
        :return: True if token deleted, else False
        """

    @classmethod
    def generate_token(cls, nbytes: int = 32) -> str:
        return secrets.token_urlsafe(nbytes=nbytes)

    def generate_and_save_token(self, nbytes: int = 32) -> str:
        token = self.generate_token(nbytes)
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Get all tokens from storage

        :return: list of tokens
        """

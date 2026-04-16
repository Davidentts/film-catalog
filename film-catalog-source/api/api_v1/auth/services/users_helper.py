import secrets
from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        Get password by username if exists

        :param username:
        :return: password string
        """

    @classmethod
    def check_password(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Check if password is correct

        :param password1:
        :param password2:
        :return:
        """
        return secrets.compare_digest(password1, password2)

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Check if password is valid

        :param username:
        :param password:
        :return:
        """
        db_password = self.get_user_password(username)
        return self.check_password(
            password1=password,
            password2=db_password,
        )

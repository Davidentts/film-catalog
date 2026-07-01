import os
import sys

import pytest


@pytest.mark.skip(reason="User schema is not implemented yet")
def test_user() -> None:
    users = {"User1": "password", "User2": ""}
    assert users["User1"] == ""


@pytest.mark.skipif(
    os.name != "nt",
    reason="This test only works on Windows",
)
def test_user_on_windows() -> None:
    assert os.name == "nt"


@pytest.mark.skipif(
    sys.platform != "posix",
    reason="This test is only for posix",
)
def test_user_on_posix() -> None:
    assert sys.platform == "posix"

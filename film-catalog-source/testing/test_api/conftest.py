import datetime
import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.api_v1.auth.services import redis_tokens
from api.api_v1.film_catalog.crud import storage
from main import app
from schemas.movie import Movie, MovieCreate


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app, headers=headers) as client:
        yield client


def create_movie() -> Movie:
    movie_in = MovieCreate(
        name="Test Movie",
        release_date=datetime.date(2020, 1, 1),
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        synopsis="A lot of words...",
        execute_producer=["Daiv", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )
    return storage.create(movie_in)


@pytest.fixture
def movie() -> Generator[Movie]:
    movie = create_movie()
    yield movie
    storage.delete(movie)

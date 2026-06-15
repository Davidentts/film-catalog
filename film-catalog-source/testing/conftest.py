import datetime
import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.film_catalog.crud import storage
from schemas.movie import Movie, MovieCreate

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for testing",
    )


def build_movie_create(slug: str) -> MovieCreate:
    return MovieCreate(
        name="Test Movie",
        release_date=datetime.date(2020, 1, 1),
        slug=slug,
        synopsis="A lot of words...",
        execute_producer=["Daiv", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )


def build_movie_create_random_slug() -> MovieCreate:
    return MovieCreate(
        name="Test Movie",
        release_date=datetime.date(2020, 1, 1),
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        synopsis="A lot of words...",
        execute_producer=["Dave", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )


def create_movie(slug: str) -> Movie:
    return storage.create(build_movie_create(slug))


def create_movie_create_random_slug() -> Movie:
    return storage.create(build_movie_create_random_slug())


@pytest.fixture
def movie() -> Generator[Movie]:
    movie = create_movie_create_random_slug()
    yield movie
    storage.delete(movie)

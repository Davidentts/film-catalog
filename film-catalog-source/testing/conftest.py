import datetime
import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.film_catalog.crud import storage
from schemas.movie import Movie, MovieCreate


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            "Environment is not ready for testing",
        )


def build_movie_create(
    slug: str,
    synopsis: str = "A lot of words...",
    name: str = "Test Movie",
) -> MovieCreate:
    return MovieCreate(
        name=name,
        release_date=datetime.date(2020, 1, 1),
        slug=slug,
        synopsis=synopsis,
        execute_producer=["Daiv", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )


def build_movie_create_random_slug(
    synopsis: str = "A lot of words...",
    name: str = "Test Movie",
) -> MovieCreate:
    return MovieCreate(
        name=name,
        release_date=datetime.date(2020, 1, 1),
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        synopsis=synopsis,
        execute_producer=["Dave", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )


def create_movie(
    slug: str,
    synopsis: str = "A lot of words...",
    name: str = "Test Movie",
) -> Movie:
    return storage.create(
        build_movie_create(
            slug=slug,
            synopsis=synopsis,
            name=name,
        ),
    )


def create_movie_random_slug(
    synopsis: str = "A lot of words...",
    name: str = "Test Movie",
) -> Movie:
    return storage.create(
        build_movie_create_random_slug(
            synopsis=synopsis,
            name=name,
        ),
    )


@pytest.fixture
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)

import datetime
import random
import string

import pytest

from api.api_v1.film_catalog.crud import MovieAlreadyExistsError, storage
from schemas.movie import Movie, MovieCreate


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


def test_create_or_raise_if_exists() -> None:
    existing_movie = create_movie()
    movie_create = MovieCreate(**existing_movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=existing_movie.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)

    assert exc_info.value.args[0] == existing_movie.slug

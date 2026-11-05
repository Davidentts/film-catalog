import pytest

from api.api_v1.film_catalog.crud import MovieAlreadyExistsError, storage
from schemas.movie import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)

    assert exc_info.value.args[0] == movie_create.slug


def test_create_twice() -> None:
    movie_create = build_movie_create_random_slug()
    # create new movie successfully
    storage.create_or_raise_if_exists(movie_create)
    # create second time, raises
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)
    storage.delete_by_slug(movie_create.slug)
    assert exc_info.value.args[0] == movie_create.slug

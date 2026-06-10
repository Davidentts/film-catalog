import pytest

from api.api_v1.film_catalog.crud import MovieAlreadyExistsError, storage
from schemas.movie import Movie, MovieCreate


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exc_info:
        storage.create_or_raise_if_exists(movie_create)

    assert exc_info.value.args[0] == movie_create.slug

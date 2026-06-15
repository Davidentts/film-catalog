import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog.crud import storage
from main import app
from schemas.movie import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        pytest.param("default", id="basic slug"),
        pytest.param("abcd", id="short slug"),
        pytest.param("abc", id="min slug"),
        pytest.param("abcdefg123", id="max slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


def test_delete(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "delete_movie",
        slug=movie.slug,
    )
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug), response.text

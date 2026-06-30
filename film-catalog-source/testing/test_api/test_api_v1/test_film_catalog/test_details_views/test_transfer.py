import pytest
from fastapi import status
from starlette.testclient import TestClient

from main import app
from schemas.movie import Movie


@pytest.mark.xfail(
    reason="Transferring movie is not implemented yet",
    raises=NotImplementedError,
)
@pytest.mark.apitest
def test_transfer_movie(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for(
        "transfer_movie",
        slug=movie.slug,
    )
    response = auth_client.post(url=url)
    assert response.status_code == status.HTTP_200_OK, response.text

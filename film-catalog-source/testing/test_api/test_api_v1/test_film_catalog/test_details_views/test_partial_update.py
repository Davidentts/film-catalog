from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog.crud import storage
from main import app
from schemas.movie import SYNOPSIS_MAX_LENGTH, Movie
from testing.conftest import create_movie_random_slug


class TestUpdatePartial:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        synopsis = request.param
        movie = create_movie_random_slug(synopsis=synopsis)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_synopsis",
        [
            pytest.param(
                "some synopsis",
                "",
                id="some-synopsis-to-no-synopsis",
            ),
            pytest.param(
                "",
                "some synopsis",
                id="no-synopsis-to-some-synopsis",
            ),
            pytest.param(
                "a" * SYNOPSIS_MAX_LENGTH,
                "",
                id="max-synopsis-to-no-synopsis",
            ),
            pytest.param(
                "",
                "a" * SYNOPSIS_MAX_LENGTH,
                id="no-synopsis-to-max-synopsis",
            ),
        ],
        indirect=["movie"],
    )
    def test_movie_update_partial(
        self,
        movie: Movie,
        new_synopsis: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie_details_partial", slug=movie.slug)
        response = auth_client.patch(
            url,
            json={"synopsis": new_synopsis},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.synopsis == new_synopsis, movie_db

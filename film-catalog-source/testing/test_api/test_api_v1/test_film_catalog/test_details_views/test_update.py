from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.film_catalog.crud import storage
from main import app
from schemas.movie import (
    NAME_MAX_LENGTH,
    SYNOPSIS_MAX_LENGTH,
    Movie,
    MovieUpdate,
)
from testing.conftest import create_movie_random_slug


class TestUpdate:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        name, synopsis = request.param
        movie = create_movie_random_slug(
            name=name,
            synopsis=synopsis,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_name, new_synopsis",
        [
            pytest.param(
                ("Default", "some synopsis"),
                "New Default",
                "New synopsis",
                id="Default",
            ),
            pytest.param(
                ("a", ""),
                "a" * NAME_MAX_LENGTH,
                "b" * SYNOPSIS_MAX_LENGTH,
                id="from-min-to-max-name-and-synopsis",
            ),
            pytest.param(
                ("a" * NAME_MAX_LENGTH, "b" * SYNOPSIS_MAX_LENGTH),
                "a",
                "",
                id="from-max-to-min-name-and-synopsis",
            ),
            pytest.param(
                ("n" * NAME_MAX_LENGTH, "s" * SYNOPSIS_MAX_LENGTH),
                "abcdef",
                "qwerty",
                id="from-max-to-some-name-and-synopsis",
            ),
            pytest.param(
                ("n", "s"),
                "abcdef",
                "qwerty",
                id="from-min-to-some-name-and-synopsis",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_name_and_synopsis_movie(
        self,
        movie: Movie,
        new_name: str,
        new_synopsis: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_movie_details", slug=movie.slug)
        movie_update = MovieUpdate(**movie.model_dump())
        movie_update.name = new_name
        movie_update.synopsis = new_synopsis
        response = auth_client.put(
            url,
            json=movie_update.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        new_data_db = MovieUpdate(**movie_db.model_dump())
        assert new_data_db == movie_update, new_data_db

import datetime
import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movie import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


def test_create_film(auth_client: TestClient) -> None:
    url = app.url_path_for("create_film")
    movie_create = MovieCreate(
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
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = MovieCreate(**response_data)
    assert received_values == movie_create, response_data


def test_create_movie_already_exists(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for("create_film")
    movie_create = MovieCreate(**movie.model_dump())
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug='{movie_create.slug}' already exists"
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too-short"),
            pytest.param(("foo-bar-spam-eggs", "string_too_long"), id="too-long"),
        ],
    )
    def movie_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self,
        movie_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_film")
        create_data, expected_error_type = movie_create_values
        response = auth_client.post(url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        ), response.text
        error_detail = response.json()["detail"][0]["type"]
        assert error_detail == expected_error_type, error_detail

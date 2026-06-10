import datetime
import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movie import MovieCreate


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

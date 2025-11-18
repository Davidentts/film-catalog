from fastapi import (
    APIRouter,
    status,
)

from api.api_v1.film_catalog.crud import storage
from schemas.movie import Movie, MovieCreate

router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "/",
    response_model=list[Movie],
)
def read_list_of_films() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)

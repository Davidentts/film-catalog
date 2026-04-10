from fastapi import APIRouter, status, Depends

from api.api_v1.film_catalog.crud import storage
from api.api_v1.film_catalog.dependencies import save_storage_state
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[Depends(save_storage_state, scope="function")],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_list_of_films() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)

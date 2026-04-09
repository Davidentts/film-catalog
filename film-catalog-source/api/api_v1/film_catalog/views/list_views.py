from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.film_catalog.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(prefix="/films", tags=["Films"])


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
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.create(movie_create)

from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .crud import film_examples
from .dependencies import get_film_by_id
from schemas.film import Movie, MovieCreate

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/")
def read_list_of_films() -> list[str]:
    return [film.name for film in film_examples]


@router.get("/{slug}")
def read_film(
    movie: Annotated[
        Movie,
        Depends(get_film_by_id),
    ],
) -> Movie:
    return movie


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    film_create: MovieCreate,
) -> Movie:
    return Movie(
        **film_create.model_dump(),
    )

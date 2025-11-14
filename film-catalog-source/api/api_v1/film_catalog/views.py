from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .crud import storage
from .dependencies import get_movie_by_slug
from schemas.film import Movie, MovieCreate

router = APIRouter(prefix="/films", tags=["Films"])


@router.get(
    "/",
    response_model=list[Movie],
)
def read_list_of_films() -> list[Movie]:
    return storage.get()


@router.get(
    "/{slug}",
    response_model=Movie,
)
def read_film(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> Movie:
    return movie


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug not found",
                    },
                },
            },
        },
    },
)
def delete_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> None:
    storage.delete(movie)

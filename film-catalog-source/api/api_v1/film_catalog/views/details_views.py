from typing import Annotated

from fastapi import Depends, APIRouter
from starlette import status

from api.api_v1.film_catalog.crud import storage
from api.api_v1.film_catalog.dependencies import get_movie_by_slug
from schemas.film import Movie

router = APIRouter(
    prefix="/{slug}",
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


@router.get(
    "/",
    response_model=Movie,
)
def read_film(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> Movie:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: Annotated[
        Movie,
        Depends(get_movie_by_slug),
    ],
) -> None:
    storage.delete(movie)

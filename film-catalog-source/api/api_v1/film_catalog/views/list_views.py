from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)

from api.api_v1.film_catalog.crud import storage, MovieAlreadyExists
from api.api_v1.film_catalog.dependencies import (
    api_token_or_basic_auth_for_unsafe_methods,
)
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        Depends(api_token_or_basic_auth_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    }
                }
            },
        }
    },
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A movie with this slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='name' already exists",
                    }
                }
            },
        }
    },
)
def create_film(
    movie_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_raise_if_exists(movie_create)
    except MovieAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_create.slug!r} already exists",
        )

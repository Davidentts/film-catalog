import datetime
from typing import Annotated
from random import randint

from annotated_types import Len

from fastapi import (
    Depends,
    APIRouter,
    status,
    Form,
)
from pydantic import Field

from .crud import film_examples
from .dependencies import get_film_by_id
from schemas.film import Film

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/")
def read_list_of_films() -> list[str]:
    return [film.name for film in film_examples]


@router.get("/{movie_id}")
def read_film(
    movie: Annotated[
        Film,
        Depends(get_film_by_id),
    ],
) -> Film:
    return movie


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    name: Annotated[
        str,
        Len(min_length=1, max_length=129),
        Form(),
    ],
    description: Annotated[
        str,
        Len(min_length=10, max_length=300),
        Form(),
    ],
    date_of_create: Annotated[
        datetime.date,
        Field(le=datetime.date.today(), description="Date of creation"),
        Form(),
    ],
) -> Film:
    return Film(
        movie_id=randint(3, 1000),
        name=name,
        description=description,
        date_of_creation=date_of_create,
    )

from typing import Annotated

from fastapi import Depends, APIRouter

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

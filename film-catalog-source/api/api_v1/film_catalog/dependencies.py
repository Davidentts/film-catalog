from http.client import HTTPException

from fastapi import (
    status,
    HTTPException,
)

from .crud import film_examples
from schemas.film import Movie


def get_film_by_id(slug: str):
    movie: Movie | None = next(
        (film for film in film_examples if film.slug == slug),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug} not found",
    )

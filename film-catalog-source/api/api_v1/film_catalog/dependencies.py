from http.client import HTTPException

from fastapi import (
    status,
    HTTPException,
)

from .crud import film_examples
from schemas.film import Film


def get_film_by_id(movie_id: int):
    movie: Film | None = next(
        (film for film in film_examples if film.movie_id == movie_id),
        None,
    )
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with id {movie_id} not found",
    )

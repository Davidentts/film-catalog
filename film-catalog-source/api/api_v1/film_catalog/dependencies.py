from http.client import HTTPException

from fastapi import (
    status,
    HTTPException,
)

from .crud import storage
from schemas.film import Movie


def get_movie_by_slug(slug: str):
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with slug {slug} not found",
    )

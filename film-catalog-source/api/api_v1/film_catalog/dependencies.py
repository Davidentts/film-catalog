import logging
from http.client import HTTPException

from fastapi import (
    status,
    HTTPException,
    BackgroundTasks,
    Request,
)

from schemas.movie import Movie
from .crud import storage

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def get_movie_by_slug(slug: str):
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage state.")
        background_tasks.add_task(storage.save_state)

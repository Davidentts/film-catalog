import logging
from http.client import HTTPException

from fastapi import (
    status,
    HTTPException,
    BackgroundTasks,
)

from schemas.movie import Movie
from .crud import storage

log = logging.getLogger(__name__)


def get_movie_by_slug(slug: str):
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug} not found",
    )


def save_storage_state(background_tasks: BackgroundTasks):
    yield
    log.info("Add background task to save storage state.")
    background_tasks.add_task(storage.save_state)

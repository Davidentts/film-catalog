import logging
from http.client import HTTPException
from typing import Annotated

from fastapi import (
    status,
    HTTPException,
    BackgroundTasks,
    Request,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from api.api_v1.auth.services import redis_tokens
from schemas.movie import Movie
from .crud import storage

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

api_static_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)


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


def validate_api_token(api_token: HTTPAuthorizationCredentials):
    if redis_tokens.token_exists(api_token.credentials):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials,
        Depends(api_static_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return None

    if api_token:
        return validate_api_token(api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You must provide an API token",
    )

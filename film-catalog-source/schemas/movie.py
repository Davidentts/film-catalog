from datetime import date
from typing import Annotated

from annotated_types import Len, Le, MaxLen
from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    name: Annotated[
        str,
        Len(min_length=1, max_length=129),
    ]
    synopsis: Annotated[
        str,
        MaxLen(max_length=1000),
    ] = ""
    execute_producer: list[str] = []
    screenwriter: str = ""
    genre: list[str] = []
    release_date: Annotated[
        date,
        Le(le=date.today()),
    ]
    original_language: str = ""
    cast: list[str] = []


class MovieCreate(MovieBase):
    """
    Model for creating a film
    """

    slug: str


class MovieUpdate(MovieBase):
    """
    Model for updating a movie
    """

    synopsis: Annotated[
        str,
        MaxLen(max_length=1000),
    ]
    execute_producer: list[str]
    screenwriter: str
    genre: list[str]
    original_language: str
    cast: list[str]


class Movie(MovieBase):
    """
    Model of a film
    """

    slug: str

from datetime import date
from typing import Annotated

from annotated_types import Len, Le, MaxLen
from pydantic import BaseModel, ConfigDict, Field


SynopsisString = Annotated[
    str,
    MaxLen(max_length=1000),
]
NameString = Annotated[
    str,
    Len(min_length=1, max_length=129),
]
ReleaseDate = Annotated[
    date,
    Le(le=date.today()),
]


class MovieBase(BaseModel):
    name: NameString
    synopsis: SynopsisString = ""
    execute_producer: list[str] = []
    screenwriter: str = ""
    genre: list[str] = []
    release_date: ReleaseDate
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

    synopsis: SynopsisString
    execute_producer: list[str]
    screenwriter: str
    genre: list[str]
    original_language: str
    cast: list[str]


class MoviePartialUpdate(MovieBase):
    """
    Model for partial updating information
    about a movie
    """

    name: NameString | None = None
    synopsis: SynopsisString | None = None
    execute_producer: list[str] | None = None
    screenwriter: str | None = None
    genre: list[str] | None = None
    release_date: ReleaseDate | None = None
    original_language: str | None = None
    cast: list[str] | None = None


class Movie(MovieBase):
    """
    Model of a film
    """

    slug: str

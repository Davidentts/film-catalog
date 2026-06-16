import datetime
from typing import Annotated

from annotated_types import Le, Len, MaxLen
from pydantic import BaseModel

SYNOPSIS_MAX_LENGTH = 1000
NAME_MAX_LENGTH = 129
NAME_MIN_LENGTH = 1

SynopsisString = Annotated[
    str,
    MaxLen(max_length=SYNOPSIS_MAX_LENGTH),
]
SlugString = Annotated[
    str,
    Len(min_length=3, max_length=10),
]
NameString = Annotated[
    str,
    Len(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH),
]
ReleaseDate = Annotated[
    datetime.date,
    Le(le=datetime.datetime.now(datetime.UTC).date()),
]


class MovieBase(BaseModel):
    name: NameString
    synopsis: SynopsisString
    execute_producer: list[str]
    screenwriter: str
    genre: list[str]
    release_date: ReleaseDate
    original_language: str
    cast: list[str]


class MovieCreate(MovieBase):
    """
    Model for creating a film
    """

    slug: SlugString
    synopsis: SynopsisString = ""
    execute_producer: list[str] = []
    screenwriter: str = ""
    genre: list[str] = []
    original_language: str = ""
    cast: list[str] = []


class MovieUpdate(MovieBase):
    """
    Model for updating a movie
    """


class MoviePartialUpdate(BaseModel):
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


class MovieRead(MovieBase):
    """
    Model for reading a movie
    """

    slug: str


class Movie(MovieBase):
    """
    Model of a film
    """

    slug: str
    notes: str = ""
    internal_rating: float = 0.0
    visits: int = 0

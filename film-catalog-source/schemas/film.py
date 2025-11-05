from datetime import date
from typing import Annotated

from annotated_types import Len, Le
from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    slug: str
    name: str
    description: str
    date_of_creation: date


class MovieCreate(MovieBase):
    """
    Model for creating a film
    """

    name: Annotated[
        str,
        Len(min_length=1, max_length=129),
    ]
    description: Annotated[
        str,
        Len(min_length=1, max_length=500),
    ]
    date_of_creation: Annotated[
        date,
        Le(le=date.today()),
    ]


class Movie(MovieBase):
    """
    Model of a film
    """

from datetime import date

from pydantic import BaseModel


class FilmBase(BaseModel):
    movie_id: int
    name: str
    description: str
    date_of_creation: date


class Film(FilmBase):
    """
    Model of a film
    """

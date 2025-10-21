from datetime import date
from http.client import HTTPException
from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    status,
    HTTPException,
    Depends,
)

from schemas.film import Film

app = FastAPI(
    title="Film Catalog API",
)

film_examples = [
    Film(
        movie_id=1,
        name="Омерзительная восьмёрка",
        description="Example",
        date_of_creation=date(2016, 1, 1),
    ),
    Film(
        movie_id=2,
        name="Бесславные ублюдки",
        description="Example",
        date_of_creation=date(2009, 8, 20),
    ),
]


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    films_url = request.url.replace(
        path="/films",
        query="",
    )
    return {
        "Message": f"Hello {name}!",
        "docs": str(docs_url),
        "List of Films": str(films_url),
    }


@app.get("/films")
def read_list_of_films() -> list[str]:
    return [film.name for film in film_examples]


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


@app.get("/film/{movie_id}")
def read_film(
    movie: Annotated[
        Film,
        Depends(get_film_by_id),
    ],
) -> Film:
    return movie

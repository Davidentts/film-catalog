from datetime import date

from pydantic import BaseModel

from schemas.film import Movie, MovieCreate


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie_in.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)


storage = MovieStorage()

storage.create(
    MovieCreate(
        slug="1",
        name="Омерзительная восьмёрка",
        description="Example",
        date_of_creation=date(2016, 1, 1),
    )
)
storage.create(
    MovieCreate(
        slug="2",
        name="Бесславные ублюдки",
        description="Example",
        date_of_creation=date(2009, 8, 20),
    )
)

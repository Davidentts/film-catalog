import logging

from pydantic import BaseModel, ValidationError

from schemas.movie import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate

from core.config import FILMS_STORAGE_FILEPATH

log = logging.getLogger(__name__)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self):
        FILMS_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
        log.info("Saved films to storage file.")

    @classmethod
    def from_state(cls):
        if not FILMS_STORAGE_FILEPATH.exists():
            return MovieStorage()
        return cls.model_validate_json(FILMS_STORAGE_FILEPATH.read_text())

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_to_movie[movie_in.slug] = movie
        self.save_state()
        log.info(
            "New movie was created with name: %s and slug: %s",
            movie.name,
            movie.slug,
        )
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_state()
        return movie


try:
    storage = MovieStorage.from_state()
    log.warning("Films storage loaded.")
except ValidationError:
    storage = MovieStorage()
    storage.save_state()
    log.warning("Rewritten storage file due to validation error.")

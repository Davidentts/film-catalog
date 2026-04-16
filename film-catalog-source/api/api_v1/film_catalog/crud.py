import logging

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)

log = logging.getLogger(__name__)

redis_movies = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieStorage(BaseModel):

    def save_movie(self, movie: Movie):
        redis_movies.hset(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(movie)
            for movie in redis_movies.hvals(name=config.REDIS_MOVIES_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis_movies.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(data)

        return None

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.save_movie(movie)
        log.info(
            "New movie was created with name: %s and slug: %s",
            movie.name,
            movie.slug,
        )
        return movie

    def delete_by_slug(self, slug: str) -> None:
        redis_movies.hdel(
            config.REDIS_MOVIES_HASH_NAME,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie


storage = MovieStorage()

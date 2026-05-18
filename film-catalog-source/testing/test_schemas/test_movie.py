import datetime
import random
import string
from os import getenv
from typing import ClassVar
from unittest import TestCase

from pydantic import ValidationError

from api.api_v1.film_catalog.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

if getenv("TESTING") != "1":
    message = "Environment is not ready for testing"
    raise OSError(message)


def create_movie() -> Movie:
    movie_in = MovieCreate(
        name="Test Movie",
        release_date=datetime.date(2020, 1, 1),
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        synopsis="A lot of words...",
        execute_producer=["Daiv", "Moris"],
        screenwriter="Alex",
        genre=["Horror", "Comedy"],
        original_language="English",
        cast=["Artur", "Morty"],
    )
    return storage.create(movie_in)


class MovieTestCreateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="test_slug",
            synopsis="A lot of words...",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie = Movie(**movie_in.model_dump())

        for field, value_in in movie_in:
            with self.subTest(
                field=field,
                value_in=value_in,
                msg=f"Create field {field} is {value_in}",
            ):
                movie_value = getattr(movie, field)
                self.assertEqual(value_in, movie_value)

    def test_movie_can_be_created_from_update_schema(self) -> None:
        movie_update = MovieUpdate(**self.movie.model_dump())
        movie_update.name = movie_update.name + " Update"
        movie_update.release_date += datetime.timedelta(days=15)
        movie_update.cast.append("Ruslan")

        storage.update(
            self.movie,
            movie_update,
        )

        self.assertEqual(
            movie_update,
            MovieUpdate(**self.movie.model_dump()),
        )

    def test_movie_can_be_updated_from_partial_schema(self) -> None:
        movie_update_partial = MoviePartialUpdate(
            name=self.movie.name + " Partial Update",
            release_date=datetime.date(2026, 1, 1),
            cast=["Ruslan"],
        )

        storage.update_partial(
            self.movie,
            movie_update_partial,
        )

        self.assertEqual(movie_update_partial.name, self.movie.name)
        self.assertEqual(movie_update_partial.release_date, self.movie.release_date)
        self.assertEqual(movie_update_partial.cast, self.movie.cast)

    def test_movie_is_not_updated_from_empty_partial_schema(self) -> None:
        movie_update_partial = MoviePartialUpdate()
        source_movie = Movie(**self.movie.model_dump())
        updated_movie = storage.update_partial(
            self.movie,
            movie_update_partial,
        )

        self.assertEqual(
            source_movie,
            updated_movie,
        )

    def test_movie_name_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exec_info:
            MovieCreate(
                name="",
                release_date=datetime.date(2020, 1, 1),
                slug="",
            )
        error_details = exec_info.exception.errors()[0]
        expected_error_type = "string_too_short"
        self.assertEqual(
            expected_error_type,
            error_details["type"],
        )

    def test_movie_partial_release_date_has_non_zero_time(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="Datetimes provided to dates should have zero time",
        ):
            partial_movie = """{"release_date": "2020-01-01 12:59:59"}"""
            MoviePartialUpdate.model_validate_json(partial_movie)


class MovieStorageGetMovieTestCase(TestCase):
    MOVIES_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_slugs = {movie.slug for movie in self.movies}
        slugs = {movie.slug for movie in movies}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                movie=movie,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )

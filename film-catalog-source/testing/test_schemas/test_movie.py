import datetime
from os import getenv
from unittest import TestCase

from pydantic import ValidationError

from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

if getenv("TESTING") != "1":
    message = "Environment is not ready for testing"
    raise OSError(message)


class MovieTestCreateTestCase(TestCase):
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
        movie = Movie(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="",
            synopsis="",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie_update = MovieUpdate(
            name="Test Movie 2.0",
            release_date=datetime.date(2026, 1, 1),
            synopsis="too many words...",
            execute_producer=["Moris"],
            screenwriter="Alex",
            genre=["Comedy"],
            original_language="Spanish",
            cast=["Marat"],
        )

        for field, value in movie_update:
            setattr(movie, field, value)

        self.assertEqual(movie_update.name, movie.name)
        self.assertEqual(movie_update.release_date, movie.release_date)
        self.assertEqual(movie_update.synopsis, movie.synopsis)
        self.assertEqual(movie_update.execute_producer, movie.execute_producer)
        self.assertEqual(movie_update.screenwriter, movie.screenwriter)
        self.assertEqual(movie_update.genre, movie.genre)
        self.assertEqual(movie_update.original_language, movie.original_language)
        self.assertEqual(movie_update.cast, movie.cast)

    def test_movie_can_be_updated_from_partial_schema(self) -> None:
        movie = Movie(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="",
            synopsis="",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie_update_partial = MoviePartialUpdate(
            name="Test Movie 3.0",
            release_date=datetime.date(2026, 1, 1),
            cast=["Ruslan"],
        )

        for field, value in movie_update_partial.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.assertEqual(movie_update_partial.name, movie.name)
        self.assertEqual(movie_update_partial.release_date, movie.release_date)
        self.assertEqual(movie_update_partial.cast, movie.cast)

    def test_movie_is_not_updated_from_empty_partial_schema(self) -> None:
        movie = Movie(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="",
            synopsis="",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie_for_update = Movie(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="",
            synopsis="",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie_update_partial = MoviePartialUpdate()

        for field, value in movie_update_partial.model_dump(exclude_unset=True).items():
            setattr(movie_for_update, field, value)

        self.assertEqual(movie.name, movie_for_update.name)
        self.assertEqual(movie.release_date, movie_for_update.release_date)
        self.assertEqual(movie.slug, movie_for_update.slug)
        self.assertEqual(movie.synopsis, movie_for_update.synopsis)
        self.assertEqual(movie.execute_producer, movie_for_update.execute_producer)
        self.assertEqual(movie.screenwriter, movie_for_update.screenwriter)
        self.assertEqual(movie.genre, movie_for_update.genre)
        self.assertEqual(movie.original_language, movie_for_update.original_language)
        self.assertEqual(movie.cast, movie_for_update.cast)

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

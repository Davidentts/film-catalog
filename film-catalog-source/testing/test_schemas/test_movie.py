import datetime
from unittest import TestCase

from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


class MovieTestCreateTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            name="Test Movie",
            release_date=datetime.date(2020, 1, 1),
            slug="test_slug",
            synopsis="",
            execute_producer=["Daiv", "Moris"],
            screenwriter="Alex",
            genre=["Horror", "Comedy"],
            original_language="English",
            cast=["Artur", "Morty"],
        )

        movie = Movie(**movie_in.model_dump())

        self.assertEqual(movie_in.name, movie.name)
        self.assertEqual(movie_in.release_date, movie.release_date)
        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.synopsis, movie.synopsis)
        self.assertEqual(movie_in.execute_producer, movie.execute_producer)
        self.assertEqual(movie_in.screenwriter, movie.screenwriter)
        self.assertEqual(movie_in.genre, movie.genre)
        self.assertEqual(movie_in.original_language, movie.original_language)
        self.assertEqual(movie_in.cast, movie.cast)

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

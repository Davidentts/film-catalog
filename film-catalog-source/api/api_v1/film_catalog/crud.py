from datetime import date

from schemas.film import Movie

film_examples = [
    Movie(
        slug="1",
        name="Омерзительная восьмёрка",
        description="Example",
        date_of_creation=date(2016, 1, 1),
    ),
    Movie(
        slug="2",
        name="Бесславные ублюдки",
        description="Example",
        date_of_creation=date(2009, 8, 20),
    ),
]

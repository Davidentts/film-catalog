from datetime import date

from schemas.film import Film

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

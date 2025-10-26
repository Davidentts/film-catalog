from fastapi import APIRouter

from .film_catalog.views import router as film_catalog_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(film_catalog_router)

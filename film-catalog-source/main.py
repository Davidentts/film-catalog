from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router

app = FastAPI(
    title="Film Catalog API",
)
app.include_router(api_router)


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

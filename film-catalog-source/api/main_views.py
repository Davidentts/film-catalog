from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def read_root(
    request: Request,
    name: str = "World",
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    films_url = request.url.replace(
        path="/api/v1/films",
        query="",
    )
    return {
        "Message": f"Hello {name}!",
        "docs": str(docs_url),
        "List of Films": str(films_url),
    }

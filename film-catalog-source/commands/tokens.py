from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services.redis_token_helper import redis_tokens


app = typer.Typer(name="token")


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check"),
    ],
):
    """
    Check if the passed token is valid - exists or not
    """
    print(
        f"Token: [bold]{token}[/bold]",
        (
            "[bold green]exists[/green bold]"
            if redis_tokens.token_exists(token)
            else "[bold red]does not exist[/bold red]"
        ),
    )

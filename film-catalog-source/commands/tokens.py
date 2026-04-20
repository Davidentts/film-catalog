from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services.redis_token_helper import redis_tokens

app = typer.Typer(
    name="token",
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Tokens management",
)


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


@app.command(name="list")
def list_tokens():
    """
    Return all tokens from storage
    """
    tokens = redis_tokens.get_tokens()
    print(Markdown("# Available API tokens"))
    print(Markdown("\n- ".join([""] + tokens)))
    print()


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="The token to add"),
    ],
):
    """
    Add a new token if not exists
    """
    if redis_tokens.token_exists(token):
        print(f"Token: [bold red]{token}[/red bold] [bold]already exists[/bold]")
        return

    redis_tokens.add_token(token)
    print(f"New token has been added successfully: [bold green]{token}[/bold green]")


@app.command()
def create(
    length: Annotated[
        int,
        typer.Argument(help="The length of the token"),
    ] = 32,
):
    """
    Create a new token and add it to storage
    """
    token = redis_tokens.generate_and_save_token(length)
    print(f"New token: [bold green]{token}[/green bold] has been added to storage")


@app.command(name="rm")
def delete(
    token: Annotated[
        str,
        typer.Argument(help="The token to delete"),
    ],
):
    """
    Remove a token from storage
    """
    if not redis_tokens.token_exists(token):
        print(f"Token: [bold red]{token}[/red bold] [bold]does not exist[/bold]")
        return

    redis_tokens.delete_token(token)
    print(
        f"Token: [bold green]{token}[/green bold] has been [bold red]removed[/red bold]"
    )

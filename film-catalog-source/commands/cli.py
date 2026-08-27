import typer

from .tokens import app as token_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich"
)
app.add_typer(token_app)

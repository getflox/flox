import click
from click import Context

from floxcore.context import Flox, Prompt
from floxcore.exceptions import ProfileException


@click.group(invoke_without_command=True)
@click.pass_obj
@click.pass_context
def profile(ctx: Context, flox: Flox):
    """
    Manage development profile
    """
    if not ctx.invoked_subcommand:
        click.secho(f"Active profile: {Prompt.colourize(flox.profile)}")


@profile.command(name="list")
@click.pass_obj
def profile_list(flox: Flox):
    """List available profiles"""
    click.echo("Environments:")

    for f in flox.settings.flox.stages:
        click.secho(("-> " if f == flox.profile else "   ") + Prompt.colourize(f))


@profile.command(name="set")
@click.argument("name")
@click.pass_obj
def set_profile(flox: Flox, name: str):
    """Change active profile"""
    if name not in flox.settings.get("global").stages:
        raise ProfileException('Unable to select "{}". Not allowed stage.'.format(name))

    flox.local.profile = name

    click.secho("Selected profile: {}".format(Prompt.colourize(name)))

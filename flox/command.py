from os import mkdir
from os.path import isdir

import click

from flox.core import Flox, colourize
from flox.core.exceptions import ProfileException


@click.command(name="set-profile")
@click.argument("name")
@click.pass_obj
def set_profile(flox: Flox, name: str):
    """Change active profile"""
    if name not in flox.settings.flox.stages:
        raise ProfileException('Unable to select "{}". Not allowed stage.'.format(name))

    if not isdir(flox.local_config_dir):
        mkdir(flox.local_config_dir)

    with open(flox.environment_file, 'w+') as f:
        f.write(name)

    flox.profile = name

    click.secho("Selected profile: {}".format(colourize(name)))


@click.command()
@click.pass_obj
def active(flox: Flox):
    """Show active profile"""
    click.secho(
        colourize(flox.profile)
    )


@click.command()
@click.pass_obj
def check(flox: Flox):
    """Check system for installed dependencies"""


@click.command()
@click.pass_obj
def profiles(flox: Flox):
    """List available profiles"""
    click.echo("All defined environments:")

    for f in flox.settings.flox.stages:
        click.secho(
            ("-> " if f == flox.profile else "   ") + colourize(f)
        )

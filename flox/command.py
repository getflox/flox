import click

from flox.core import Flox, colourize


@click.command()
@click.argument("name")
@click.pass_obj
def select(flox: Flox, name: str):
    """Change active profile"""
    if name not in flox.settings.stylist.get('stages', []):
        raise InvalidProfileName('Unable to select "{}". Not allowed stage.'.format(name))

    with open(flox.environment_file, 'w+') as f:
        f.write(name)

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

    for f in flox.settings.stylist.get('stages', []):
        click.secho(
            ("-> " if f == flox.profile else "   ") + colourize(f)
        )



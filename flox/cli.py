import click
from click_plugins import with_plugins
from click_shell import shell
from pkg_resources import iter_entry_points

from flox.core import Flox

instance = Flox()

CONTEXT_SETTINGS = dict(
    auto_envvar_prefix='FLOX',
    obj=instance
)


@with_plugins(iter_entry_points('flox.cli_plugins'))
@shell(prompt=instance.prompt, context_settings=CONTEXT_SETTINGS)
def cli():
    """Main command"""


@cli.command()
@click.pass_obj
def select(ctx: Flox):
    """Main - Subcommand that does something."""
    ctx.profile = 'live'

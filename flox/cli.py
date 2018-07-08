import click
from click_plugins import with_plugins
from click_shell import shell
from pkg_resources import iter_entry_points

from flox.command import select, check, profiles, active
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


cli.add_command(select)
cli.add_command(check)
cli.add_command(profiles)
cli.add_command(active)

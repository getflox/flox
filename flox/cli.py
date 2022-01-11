from os import getcwd

import click
from click_plugins import with_plugins
from click_shell import shell
from pkg_resources import iter_entry_points

from flox.config.command import config
from flox.info.command import flox_info
from flox.plugins.command import plugin
from flox.profile.command import profile
from flox.project.command import project
from floxcore.context import Flox, locate_project_root
from floxcore.exceptions import FloxException

instance = Flox()

CONTEXT_SETTINGS = dict(auto_envvar_prefix="FLOX", obj=instance)


@with_plugins(iter_entry_points("flox.plugin.command"))
@shell(prompt=instance.prompt, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    Consistent project management and automation with flox
    """
    if not instance.initiated and not ctx.invoked_subcommand:
        raise FloxException("Unable to load interactive shell for uninitialised project.")


cli.add_command(config)
cli.add_command(plugin)
cli.add_command(project)
if locate_project_root(getcwd()):
    cli.add_command(flox_info)
    cli.add_command(profile)

Flox.plugins.add_commands(cli)

if __name__ == "__main__":
    cli()

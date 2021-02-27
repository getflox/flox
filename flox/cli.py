from os import getcwd

from click_plugins import with_plugins
from click_shell import shell
from pkg_resources import iter_entry_points

from flox.config.command import config
from flox.info.command import flox_info
from flox.plugins.command import plugin
from flox.profile.command import profile
from flox.project.command import project
from floxcore.context import Flox, locate_project_root

instance = Flox()

CONTEXT_SETTINGS = dict(auto_envvar_prefix="FLOX", obj=instance)


@with_plugins(iter_entry_points("flox.plugin.command"))
@shell(prompt=instance.prompt, context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Consistent project management and automation with flox
    """


cli.add_command(config)
cli.add_command(plugin)
cli.add_command(project)
if locate_project_root(getcwd()):
    cli.add_command(flox_info)
    cli.add_command(profile)

Flox.plugins.add_commands(cli)

if __name__ == "__main__":
    cli()

import re
from dataclasses import astuple
from typing import List

import click
from click import Context

from flox.plugins.manager import search, PluginDefinition, install, list_installed, uninstall
from floxcore.console import success
from floxcore.context import Flox
from floxcore.exceptions import PluginException
from floxcore.utils.table import BaseTable


class PluginsTable(BaseTable):
    HEADER = list(PluginDefinition.__annotations__.keys())

    @classmethod
    def build(cls, plugins: List[PluginDefinition]):
        return cls([PluginsTable.HEADER] + [astuple(p) for p in plugins])


def build_plugin_name(name: str):
    # @TODO Add tests
    if name.startswith(("https://", "http://", "git://", "git+")):
        """
        Handle cases like:
        - https://github.com/getflox/flox-jira
        - http://github.com/getflox/flox-jira
        - git://github.com/getflox/flox-jira.git
        - git+https://github.com/getflox/flox-jira
        - https://github.com/getflox/flox-jira.git
        and combinations of those.
        """
        install_name = name
        if not name.endswith(".git"):
            install_name = name + ".git"
        if not name.startswith("git+"):
            install_name = "git+" + name
    elif re.match(r"\w+/\w+", name):
        """
        Handle cases like:
        - getflox/flox-jira
        """
        install_name = f"git+https://github.com/{name}.git"
    else:
        """
        Handle cases like:
        - flox-jira
        """
        try:
            plugin = next(search(name))
            install_name = f'git+{plugin.url}.git'
        except StopIteration:
            raise PluginException(f'Plugin "{name}" not found.')

    return install_name


@click.group(invoke_without_command=True)
@click.pass_context
@click.pass_obj
def plugin(flox: Flox, ctx: Context):
    """Manage plugins"""
    if ctx.invoked_subcommand:
        return

    plugins = list_installed(flox)
    if not plugins:
        raise PluginException("No plugins installed.")

    click.echo(PluginsTable.build(plugins).table)


@plugin.command(name="uninstall")
@click.argument("name")
def plugin_uninstall(name):
    """Uninstall installed plugin"""
    uninstall(name)

    success(f'Plugin {name} uninstalled.')


@plugin.command(name="install")
@click.argument("name")
def plugin_install(name: str):
    """Install plugin"""
    install(build_plugin_name(name))

    success(f'Plugin "{name}" installed.')


@plugin.command(name="search")
@click.argument("name")
def plugin_search(name: str):
    """Search plugin"""

    result = search(name)
    table = PluginsTable.build(result).table.replace(name, click.style(name, fg="red"))

    click.echo(table)

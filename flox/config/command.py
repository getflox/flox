import hashlib
from os.path import join, isdir
from shutil import rmtree

import anyconfig
import click
from click import Abort
from loguru import logger

from flox.config.parameters import interactive_parameters
from flox.config.remotes import fetch_remote
from flox.config.secrets import interactive_secrets
from floxcore import CONFIG_DIRS
from floxcore.command import execute_stages
from floxcore.console import info, warning, warning_box, success_box, success
from floxcore.context import Flox
from floxcore.exceptions import MissingPluginException, ConfigurationException


@click.group(name="config", invoke_without_command=True)
@click.option(
    "--scope",
    help="Save configuration to given scope",
    type=click.Choice(["system", "user", "project"], case_sensitive=False),
    default="project",
)
@click.option("--profile", help="Save configuration for given profile. "
                                "By default settings are stored for all profiles in given scope.")
@click.option("--without-secrets", help="Skip secrets configuration", default=False, is_flag=True)
@click.option("--without-parameters", help="Skip parameters configuration", default=False, is_flag=True)
@click.option("--plugin", multiple=True)
@click.pass_obj
@click.pass_context
def config(ctx, flox: Flox, scope, profile, plugin, without_secrets, without_parameters):
    """
    Run configuration wizard for flox.
    """
    if ctx.invoked_subcommand:
        return

    if not plugin:
        raise ConfigurationException("You need to specify at least one plugin to be configured",
                                     extra="Use flox config --plugin=<plugin-name>")

    if not flox.initiated and scope == "project":
        warning("Unable to use scope project outside of project directory. Changing scope to 'user'")
        scope = "user"

    for name in plugin:
        if not flox.plugins.has(name):
            raise MissingPluginException(name)

        info(f"Starting configuration of {name} for '{scope}' scope" + (f" and '{profile}' profile" if profile else ""))

        if not without_parameters:
            interactive_parameters(flox, name, flox.plugins.get(name), scope, profile)

        if not without_secrets:
            if scope == "system" and not click.confirm(warning("Flox can't manage secrets on the system level. "
                                                               "If you like to continue all secrets would be stored at "
                                                               "user level", no_print=True)):
                raise Abort
            interactive_secrets(flox, name, flox.plugins.get(name), scope, profile)

        execute_stages(
            flox, "configuration_change", features=[name]
        )


@config.command(name="show")
@click.pass_obj
def show(flox: Flox):
    """Display current configuration"""
    for section, settings in flox.settings.items():
        info(f"Configuration of '{section}'")
        click.echo(anyconfig.dumps(settings, ac_parser="toml"))


@config.command(name="add")
@click.argument("remote")
@click.pass_obj
def remotes_add(flox: Flox, remote):
    """Add new remote configuration"""
    # if flox.remotes.has(remote):
    #     raise ConfigurationException(f"Remote configuration '{remote}' already exists")

    warning_box("Remote configuration sources are potentially dangerous, you should only add configuration "
                "from trusted sources")
    if not click.confirm(click.style(f"Would you still like to add {remote} as configuration source?", fg="yellow")):
        raise Abort

    config_type = "local"
    if remote.lower().startswith(("http://", "https://")):
        config_type = "remote"
    elif remote.lower().startswith("git") or remote.endswith(".git"):
        config_type = "git"

    flox.remotes.set(remote, dict(
        type=config_type,
        hash=hashlib.sha256(remote.encode("UTF-8")).hexdigest()
    ))

    fetch_remote(flox, remote)

    success_box(f"Remote source '{remote}' has been added as a configuration source")


@config.command(name="remove")
@click.argument("remote")
@click.pass_obj
def remotes_remove(flox: Flox, remote):
    """Remove remote configuration"""
    if not flox.remotes.has(remote):
        raise ConfigurationException(f"Unable to find '{remote}' remote configuration")

    remote_config_dir = join(CONFIG_DIRS.get("user"), "externals", flox.remotes.get(remote).get("hash"))
    if remote_config_dir.startswith(CONFIG_DIRS.get("user")) and isdir(remote_config_dir):
        logger.debug(f"Removed local cache of remote config: {remote_config_dir}")
        rmtree(remote_config_dir)

    flox.remotes.remove(remote)

    success_box(f"Remote source '{remote}' has been removed")


@config.command(name="update-remotes")
@click.pass_obj
def remotes_update(flox: Flox):
    """Update all remote configurations"""

    for source in flox.remotes.all().keys():
        fetch_remote(flox, source)
        success(f"Updated: {source}")

    success_box(f"Remote sources updated")

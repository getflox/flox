import re
from os import makedirs, getcwd
from os.path import join, abspath

import click
from slugify import slugify

from floxcore.command import execute_stages
from floxcore.console import info_box
from floxcore.context import Flox
from floxcore.exceptions import PluginException


def initiate_project_structure(flox: Flox, name, description, tag, features):
    if not name:
        name = click.prompt("Enter project name")

    if not description:
        description = click.prompt("Enter project description")

    name = re.sub(r"\s+", " ", name)
    project_id = slugify(name)
    project_dir = join(getcwd(), project_id)

    target = click.prompt("Target directory", default=project_dir)
    if target != project_dir:
        project_dir = abspath(target)

    makedirs(join(project_dir, ".flox"), exist_ok=True)

    new_project = Flox(project_dir)
    new_project.meta.id = project_id
    new_project.meta.name = name
    new_project.meta.description = description
    new_project.meta.tags = tag
    new_project.meta.features = features

    return new_project


@click.group(invoke_without_command=True, with_plugin_selector=True, params_from=["flox_project"])
@click.option("--name", help="Project name")
@click.option("--description", help="Longer project description")
@click.option("--tag", help="Tag, only used by plugins which are able to use it.", multiple=True)
@click.pass_obj
@click.pass_context
def project(ctx, flox: Flox, name: str, description: str, tag: list, **kwargs):
    """Initialise new project with flox"""
    if ctx.invoked_subcommand:
        return

    if flox.initiated and not click.confirm("Trying to initialise already initialised project. Are you sure you would like to proceed?"):
        raise click.Abort()

    features = [k.replace("with_", "") for k, v in kwargs.items() if k.startswith("with_") and v]

    project_flox = flox

    if not flox.initiated:
        project_flox = initiate_project_structure(flox, name, description, tag, features)

    execute_stages(project_flox, "project",
                   features=kwargs.get("scope", []) or project_flox.meta.features, **kwargs)


@project.command(name="add")
@click.argument("feature")
@click.pass_obj
def project_add(flox: Flox, feature: str):
    """Add plugin features to active project"""
    if feature in flox.meta.features:
        raise PluginException(
            f"Plugin {feature} is already enabled for '{flox.meta.name}' project"
        )

    flox.meta.features.append(feature)
    flox.meta._save()

    execute_stages(flox, "project", options={feature: True})


@project.command(name="remove")
@click.argument("feature")
@click.pass_obj
def project_remove(flox: Flox, feature: str):
    """Remove plugin features from active project"""
    if feature not in flox.meta.features:
        raise PluginException(
            f"Plugin {feature} is not enabled for '{flox.meta.name}' project",
            extra=f"You can list installed plugins with `flox info`"
        )

    flox.meta.features.remove(feature)
    flox.meta._save()

    info_box(
        message=f"'{feature}' integration has been removed from current project",
        extra="Please note that flox only disabled any future plugin actions, it's your responsibility "
              "to remove / modify any relevant code from your project."
    )

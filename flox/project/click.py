from os import getcwd, mkdir
from os.path import join, isdir, isfile

import click
import humps
import yaml
from floxcore import FloxContext

from flox.profile.profiles import get_profile
from flox.project.apply import apply_settings
from flox.project.create import create_project


@click.command()
@click.pass_obj
def apply(obj: FloxContext):
    """Configure project resources using values provided in the configuration file"""
    apply_settings(obj)


@click.command()
@click.pass_obj
@click.option("--name", prompt=True)
@click.option("--description", prompt=True)
@click.argument("profile")
def create(obj: FloxContext, profile, name, description):
    """Create new project using provided profile"""
    profile = get_profile(profile)

    create_project(obj, name=name, description=description, profile=profile)

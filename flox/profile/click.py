from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from flox.profile.profiles import get_profiles


@click.group()
def profiles():
    """Manage configuration profiles"""


@profiles.command(name="list")
def profiles_list():
    """List available profiles"""

    table = Table()

    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    for profile in get_profiles():
        table.add_row(profile.name, profile.description)

    console = Console(width=120)
    console.print(table)


@profiles.group()
def sources():
    """Manage profile sources"""


@sources.command(name="download")
@click.argument("path")
def source_download(path):
    """Downloads profile from given URL"""
    directory = Path.joinpath(Path.home(), ".flox", "cache", "profiles")
    file = Path(path)

    Path(directory).mkdir(parents=True, exist_ok=True)
    Path(Path.joinpath(directory, file.name)).write_text(file.read_text())

import click

from floxcore.context import Flox
from floxcore.utils.table import BaseTable


@click.command(name="info")
@click.pass_obj
def flox_info(flox: Flox):
    """Display project information"""
    labels = dict(
        id="Project ID", name="Project Name", description="Description", tags="Tags"
    )

    data = [(
        click.style("Attribute".ljust(30), fg="green"),
        click.style("Value".ljust(30), fg="green")
    )]
    for name, label in labels.items():
        data.append((label, flox.meta.get(name)))

    table = BaseTable(data)

    click.echo("")
    click.echo(table.table)

    click.echo("")
    data = [(
        click.style("Plugin".ljust(30), fg="green"),
        click.style("Description".ljust(30), fg="green")
    )]
    for name in flox.meta.features:
        data.append((name, flox.plugins.get(name)))

    table = BaseTable(data)
    click.echo(table.table)
    click.echo("")

import os

import click
from click_plugins import with_plugins
from floxcore import FloxContext
from pkg_resources import iter_entry_points

from .project.click import apply, create
from .profile.click import profiles

context = FloxContext(plugins=iter_entry_points("flox.plugin"))


@with_plugins(context.plugins)
@click.group()
@click.pass_context
@click.option("--work-dir", default=os.getcwd(), type=click.Path())
def cli(ctx, work_dir):
    """
    Consistent project management and automation with flox
    """
    ctx.obj = context
    ctx.obj.work_dir = work_dir
    ctx.obj.load()


cli.add_command(apply)
cli.add_command(create)
cli.add_command(profiles)

if __name__ == "__main__":
    cli()

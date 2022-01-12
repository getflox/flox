import click
from loguru import logger
from schema import Optional

from floxcore.config import ParamDefinition, Configuration
from floxcore.console import info, warning, prompt
from floxcore.utils.functions import list_get
from floxcore.utils.table import BaseTable


class GlobalConfiguration(Configuration):
    def parameters(self):
        return (
            ParamDefinition("stages", "List of the project environments", multi=True, default=["dev", "test", "prod"]),
        )

    def schema(self):
        schemas = {Optional("stages", default=["production", "test", "integration"]): list}


def apply_diff(settings, diff):
    logger.debug(f"Applying diff: {diff} on {settings}")
    for action, field, changes in diff:
        logger.debug(f"Processing change with action: '{action}', on field: '{field}' and changes: '{changes}'")
        if action == "add":
            for index, value in changes:
                if field == "":
                    settings[index] = value
                else:
                    settings[field].insert(index, value)
        elif action == "change":
            if isinstance(field, str):
                if changes[1]:
                    settings[field] = changes[1]
                else:
                    settings.pop(field, None)
            elif changes[1] is None:
                del settings[field]
            else:
                settings[field[0]][field[1]] = changes[1]
        elif action == "remove":
            for index, value in changes:
                if field == "":
                    settings.pop(index, None)
                else:
                    settings[field].pop(index)
    return settings



def show_diff(parameters, current_settings, new_settings):
    """Show difference between existing and new configuration"""

    data = [("Key", "Old value", "New value")]
    for param in [p for p in parameters if
                  new_settings.get(p.name) != current_settings.get(p.name)]:
        data.append((
            param.description,

            click.style(str(current_settings.get(param.name)), fg="red") if current_settings.get(
                param.name) is not None else "-",

            click.style(str(new_settings.get(param.name)), fg="green") if new_settings.get(
                param.name) is not None else "-"
        ))

    if len(data) == 1:
        warning("No configuration changes detected")
        return False

    click.secho("\nNew configuration:\n", fg="green")
    table = BaseTable(data)
    click.echo(table.table + "\n")

    return click.confirm(click.style("Save plugin settings?", fg="green"))


def configuration():
    return GlobalConfiguration()

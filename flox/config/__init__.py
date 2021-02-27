import click
from loguru import logger
from schema import Optional

from floxcore.config import ParamDefinition, Configuration
from floxcore.console import info, warning
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


def prompt(param: ParamDefinition):
    func = click.confirm if param.boolean else click.prompt

    val = None
    if param.multi:
        val = []
        info(f"'{param.description}' configuration is accepting multiple values, "
             f"each in new line, enter empty value to end input, '-' to delete value")

    i = 0
    while True:
        current_value = list_get(param.default, i, "") if param.multi else param.default
        str_val = func(click.style(" \u2192 " + param.description, fg="green"), default=current_value)

        if param.multi and str_val and str_val != "-":
            val.append(str_val)
        elif not param.multi:
            val = str_val

        # hack to avoid prompt in same line
        if str_val == current_value:
            click.echo("")

        stdout = click.get_text_stream("stdout")
        stdout.write("\033[F")
        stdout.write("\033[K")

        if str_val:
            click.echo(f" \u2714 {param.description}: {str_val}")

        i += 1
        if not str_val or not param.multi:
            break

    if param.filter_empty and not param.boolean and not val:
        return None

    return val


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

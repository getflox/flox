import os
from os.path import join, isfile, dirname
from typing import Tuple

import anyconfig
import click
import dictdiffer

from flox.config import prompt, show_diff, apply_diff
from floxcore import CONFIG_DIRS
from floxcore.config import ParamDefinition, load_settings
from floxcore.console import info
from floxcore.context import Flox
from floxcore.plugin import Plugin


def with_settings(settings: dict, parameters: Tuple[ParamDefinition]) -> Tuple[ParamDefinition]:
    """Set existing configuration values as defaults for parameters"""
    for param in parameters:
        param.default = settings.get(param.name, param.default)
        yield param


def save_settings(flox, name, scope, profile, settings, remove=None):
    """Save new configuration settings to scoped file"""
    if remove is None:
        remove = []

    file_name = f"settings.{profile}.toml" if profile else "settings.toml"
    file_path = join(CONFIG_DIRS.get(scope, join(flox.working_dir, ".flox")), file_name)

    current = open(file_path).read() if isfile(file_path) else ""

    scoped_config = anyconfig.loads(current, ignore_missing=True, ac_parser="toml")
    section = scoped_config.get(name, {})
    section.update(settings)

    for r in remove:
        section.pop(r, None)

    scoped_config[name] = section

    os.makedirs(dirname(file_path), exist_ok=True)
    with open(file_path, "w+") as f:
        anyconfig.dump(scoped_config, f, ac_parser="toml")

    info(f"Configuration saved: {click.format_filename(file_path)}")


def build_new_settings(settings, name, new_values):
    dd = list(dictdiffer.diff(settings.get(name).to_dict(), new_values))
    new_settings = apply_diff(dict(settings.get(name).to_dict()), dd)
    has_changes = bool(dd)
    removals = []
    for removal in next(filter(lambda x: x[0] == "remove", dd), [None, None, []])[2]:
        new_settings.pop(removal[0], None)
        removals.append(removal[0])
        has_changes = True

    return new_settings, has_changes, removals


def interactive_parameters(flox: Flox, name: str, plugin: Plugin, scope, profile):
    configuration = plugin.configuration()
    settings = load_settings(Flox.plugins, flox.initiated, flox.working_dir, profile)

    new_values = {}
    for param in with_settings(settings.get(name), configuration.parameters()):
        if param.depends_on and not new_values.get(param.depends_on):
            continue

        if param.value_of:
            param.default = param.default or new_values.get(param.value_of)

        new_values[param.name] = prompt(param)

    new_settings, has_changes, removals = build_new_settings(settings, name, new_values)

    if show_diff(configuration.parameters(), settings.get(name), new_settings):
        save_settings(flox, name, scope, profile, new_settings, removals)

from typing import List

import dictdiffer

from flox.config import prompt, show_diff, apply_diff
from floxcore.config import ParamDefinition
from floxcore.console import info
from floxcore.context import Flox
from floxcore.plugin import Plugin

from loguru import logger


def save_secrets(flox: Flox, scope: str, profile: str, settings: dict):
    for name, value in settings.items():
        if not value:
            logger.debug(f"Ignore empty secret for {name}")
            continue
        logger.debug(f"Storing secret `{name}` with value `{value}` in `{scope}` scope")
        flox.secrets.put(name, value, scope=scope, profile=profile)

    info(f"Updated {len(settings)} secrets")


def with_secrets(flox: Flox, plugin: str, scope, profile, parameters: List[ParamDefinition]):
    for param in parameters:
        param.name = f"{plugin}_{param.name}"
        param.default = flox.secrets.getone(param.name, profile=profile) or param.default

    return parameters


def interactive_secrets(flox: Flox, name: str, plugin: Plugin, scope, profile):
    configuration = plugin.configuration()

    new_values = {}
    secrets = with_secrets(flox, name, scope, profile, configuration.secrets())

    for param in secrets:
        new_values[param.name] = prompt(param)

    current_settings = dict(filter(lambda y: y[1], map(lambda x: (x.name, x.default), secrets)))
    diff = list(dictdiffer.diff(current_settings, new_values))
    new_settings = apply_diff(current_settings.copy(), diff)

    if show_diff(secrets, current_settings, new_settings):
        save_secrets(flox, scope, profile, new_settings)

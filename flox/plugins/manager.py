from typing import List

import click
import requests
from plumbum import ProcessExecutionError
from requests import HTTPError

from floxcore.context import Flox
from floxcore.exceptions import PluginException
from floxcore.plugin import PluginDefinition


def _request() -> dict:
    try:
        r = requests.get("https://api.github.com/search/repositories?q=org:getflox+is:public+topic:flox-plugin")
        r.raise_for_status()
        result = r.json()
    except HTTPError as e:
        raise PluginException(f'Unable to fetch list of repositories from github: "{e}".') from e
    except AttributeError as e:
        raise PluginException(f'Unable to parse github repositories list: "{e}"') from e

    return result


def search(name: str) -> List[PluginDefinition]:
    result = _request()

    # @TODO handle `incomplete_results`
    for item in [i for i in result.get("items", []) if name in i["name"]]:
        yield PluginDefinition(item["name"], item["description"], item["html_url"])


def install(url: str) -> None:
    try:
        from plumbum.cmd import pip

        ((pip["install", url]) > click.get_binary_stream('stdout'))()
    except ImportError:
        raise PluginException(f'You do not have "pip" installed.')
    except ProcessExecutionError as e:
        raise PluginException(f'Unable to install plugin: "{e.stderr}".')


def uninstall(name: str) -> None:
    try:
        from plumbum.cmd import pip

        ((pip["uninstall", name, "-y"]) > click.get_binary_stream('stdout'))()
    except ImportError:
        raise PluginException(f'You do not have "pip" installed.')


def list_installed(flox: Flox) -> List[PluginDefinition]:
    return flox.plugins.plugins.values()

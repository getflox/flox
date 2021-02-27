from os import makedirs
from os.path import join, basename
from urllib.parse import urlparse

import requests
from loguru import logger

from floxcore import CONFIG_DIRS
from floxcore.context import Flox
from floxcore.exceptions import ConfigurationException
from floxcore.remotes import fetch_remote_git, copy_local_config


def fetch_remote_file(flox: Flox, storage, source):
    logger.debug(f"Adding {source} as external storage with http requests")
    sources = [source] + [source.replace(".toml", f".{f}.toml") for f in flox.settings.get("global").stages]

    for s in sources:
        try:
            logger.debug(f"Trying to download '{s}'")
            response = requests.get(s)
            response.raise_for_status()

            destination = join(storage, basename(urlparse(s).path))
            with open(destination, "wb+") as f:
                f.write(response.content)

            logger.debug(f"Saved remote config into: '{destination}'")

        except Exception as e:
            if s == source:
                raise ConfigurationException("Unable to fetch remote configuration", extra=str(e))

            logger.debug(f"Failed to download external config with: {e}")


def fetch_remote(flox: Flox, remote):
    source = flox.remotes.get(remote)

    storage = join(CONFIG_DIRS.get("user"), "externals", str(source.get("hash")))
    makedirs(storage, exist_ok=True)

    if source.get("type") == "git":
        return fetch_remote_git(flox, storage, remote)
    elif source.get("type") == "local":
        return copy_local_config(flox, storage, remote)
    else:
        return fetch_remote_file(flox, storage, remote)

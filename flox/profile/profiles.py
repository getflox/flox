from typing import Generator

import yaml
from loguru import logger

from flox.profile.sources import get_sources, Profile


def get_profiles() -> Generator[Profile, None, None]:
    for source in get_sources():
        for profile in source.profiles():
            with open(profile.source, "r") as stream:
                try:
                    source_profile: dict = yaml.safe_load(stream)
                    profile.description = source_profile.get("meta", {}).get("description")
                except yaml.YAMLError as e:
                    logger.exception(e)
            yield profile


def get_profile(name) -> Profile:
    for profile in get_profiles():
        if profile.name == name:
            return profile

from abc import ABC, abstractmethod
from os import listdir
from os.path import join, dirname, realpath, isfile
from pathlib import Path
from typing import List


class Profile(object):
    def __init__(self, name, description, source) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.source = source


class Repository(ABC):
    def __init__(self, location):
        self.location = location

    @abstractmethod
    def profiles(self):
        return


class LocalRepository(Repository):
    def profiles(self):
        for profile in [profile for profile in listdir(self.location) if
                        isfile(join(self.location, profile)) and profile.endswith(".yml")]:
            yield Profile(name=profile.replace(".yml", ""), source=join(self.location, profile), description="-")


class FloxRepository(LocalRepository):
    def __init__(self):
        super().__init__(location=realpath(join(dirname(__file__), "..", "..", "profiles")))


class UserCacheRepository(LocalRepository):
    def __init__(self):
        super().__init__(location=str(Path.joinpath(Path.home(), ".flox", "cache", "profiles")))


def get_sources() -> List[Repository]:
    return [UserCacheRepository(), FloxRepository()]

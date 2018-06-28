import os
from os.path import join, realpath, isfile

from git import Repo, InvalidGitRepositoryError

from flox.core import config
from flox.core.utils import colourize, locate_project_root


class Flox:
    CONFIG_FILE_NAME = 'config.yml'

    def __init__(self):
        self.cwd = os.getcwd()
        self.working_dir = realpath(locate_project_root() or self.cwd)
        self.settings = config.get(self.working_dir)
        self.name = self._name()
        self.profile = self._profile()

    @property
    def environment_file(self):
        return join(self.local_config_dir, 'environment')

    @property
    def local_config_dir(self):
        return join(self.working_dir, ".flox")

    @property
    def config_file(self):
        return join(self.local_config_dir, Flox.CONFIG_FILE_NAME)

    @property
    def prompt(self):
        return Prompt(self)

    def _name(self):
        try:
            name = Repo(self.working_dir) \
                .remote('origin') \
                .url \
                .split('/')[-1] \
                .replace(".git", '')

            for _rep in self.settings.get('flox', {}).get('name_exclusion', []):
                name = name.replace(_rep, '')

        except InvalidGitRepositoryError:
            name = 'unknown'

        return str(name)

    def _profile(self):
        if not isfile(self.environment_file):
            return 'local'

        with open(self.environment_file) as f:
            return f.readline().strip()


class Prompt:
    def __init__(self, flox: Flox) -> None:
        self.flox = flox

    def __repr__(self):
        return '{name}@{profile}> '.format(name=self.flox.name, profile=colourize(self.flox.profile))

from os import getcwd, mkdir
from os.path import join, isdir, isfile

import humps
import yaml
from floxcore import FloxContext
from floxcore.plugin import Stage
from floxcore.ui import Output

from flox.plugin import core
from flox.project.workflow import apply_stages


def update_flox_config(flox: FloxContext, output: Output, **kwargs):
    """Update local profile config"""
    with open(flox.profile_file, "w+") as f:
        yaml.dump({**{"project": flox.project.as_dict()}, **flox.profile.to_dict()}, f)

    output.success(f"Saved project settings: {flox.profile_file}")


def create_project(flox: FloxContext, name, description, profile):
    project_id = humps.kebabize(name)
    work_dir = join(getcwd(), project_id)

    if not isdir(work_dir):
        mkdir(work_dir)

    if not isfile(join(work_dir, ".flox")):
        with open(join(work_dir, ".flox"), "w+") as f:
            settings = yaml.safe_load(open(profile.source, "r"))
            settings.pop("meta", None)
            settings["project"] = dict(
                id=project_id,
                name=name,
                description=description
            )
            yaml.dump(settings, f)

    flox.work_dir = work_dir
    flox.load()

    stages = flox.project.stages
    stages.append(Stage(callback=update_flox_config, priority=99999, plugin=core))
    apply_stages(flox, stages)

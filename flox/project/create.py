from os import getcwd, mkdir
from os.path import join, isdir, isfile

import click
import humps
import yaml
from floxcore import FloxContext
from floxcore.exceptions import PluginException
from floxcore.ui import tqdm
from loguru import logger


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
    stream = click.get_text_stream("stdout")
    outputs = {}
    with tqdm(total=len(stages), file=stream) as t:
        for stage in stages:
            t.set_description(str(stage))
            try:
                outputs.update(stage(flox=flox, output=t, **outputs, **flox.profile.get(stage.plugin.name)) or {})
            except PluginException as e:
                t.error(str(stage) + f": {str(e).strip()}")
            except Exception as e:
                t.error(str(stage) + f": {str(e).strip()}")
                logger.exception(e)
            t.update(1)

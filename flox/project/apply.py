import click
from floxcore import FloxContext
from floxcore.ui import tqdm
from loguru import logger

from floxcore.exceptions import PluginException


def apply_settings(flox: FloxContext):
    stages = flox.project.stages

    stream = click.get_text_stream("stdout")
    outputs = {}
    with tqdm(stages, total=len(stages), file=stream) as t:
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

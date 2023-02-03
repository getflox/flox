from typing import List

import click
from loguru import logger

from floxcore import FloxContext
from floxcore.exceptions import PluginException
from floxcore.plugin import Stage
from floxcore.ui import tqdm


def apply_stages(flox: FloxContext, stages: List[Stage]):
    stream = click.get_text_stream("stdout")
    outputs = {}
    with tqdm(total=len(stages), file=stream) as t:
        for stage in stages:
            t.set_description(str(stage))
            try:
                outputs.update(stage(flox=flox, output=t, **outputs, **flox.profile.get(stage.plugin.name, {})) or {})
            except PluginException as e:
                t.error(str(stage) + f": {str(e).strip()}")
            except Exception as e:
                t.error(str(stage) + f": {str(e).strip()}")
                logger.exception(e)
            t.update(1)

        t.set_description("Done")

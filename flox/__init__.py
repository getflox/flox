import sys
from loguru import logger

import floxcore
from flox.click import patched
from flox.config import GlobalConfiguration
from floxcore.plugin import Plugin

# we use native system options to detect verbose mode as soon as possible so we can get right logging level
# even before click framework kicks in, or any logger actions are called
logger.remove()
floxcore.DEBUG = "-v" in sys.argv
logger.add(sys.stderr, level="DEBUG" if floxcore.DEBUG else "WARNING")


class GlobalPlugin(Plugin):
    def configuration(self):
        return GlobalConfiguration()


def plugin():
    return GlobalPlugin()

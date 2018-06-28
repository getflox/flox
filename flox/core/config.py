from os.path import join, expanduser

import anyconfig
from box import Box
from schema import Schema, And, Optional

schema = {
    Optional('flox'): {
        Optional('stages'): list,
        Optional('name_exclusion'): list,
    }
}

conform = Schema(schema, ignore_extra_keys=True).validate


def get(root_dir):
    from pkg_resources import iter_entry_points
    iter_entry_points('flox.cli_plugins.config')

    config = anyconfig.load(
        [
            '/etc/flox/config.yaml',
            join(expanduser('~'), '.flox', 'config.yaml'),
            join(root_dir, '.flox/config.yaml')
        ],
        ignore_missing=True,
        ac_parser="yaml"
    )

    return Box(conform(config), default_box=True)

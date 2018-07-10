from os.path import join, expanduser

import anyconfig
from box import Box
from schema import Schema, Optional


def get(root_dir):
    config = anyconfig.load(
        [
            '/etc/flox/config.yaml',
            join(expanduser('~'), '.flox', 'config.yaml'),
            join(root_dir, '.flox/config.yaml')
        ],
        ignore_missing=True,
        ac_parser="yaml"
    )

    from pkg_resources import iter_entry_points
    schemas = {
        'flox': {
            Optional('stages', default=['production', 'test', 'integration']): list,
            Optional('name_exclusion'): list,
        }
    }

    for entrypoints in iter_entry_points('flox.cli_plugins.config'):
        schemas[entrypoints.name] = entrypoints.load()()

    for name, schema in schemas.items():
        config[name] = Schema(schema, ignore_extra_keys=True).validate(config.get(name, {}))

    return Box(config, default_box=True)

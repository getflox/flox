import click
from click import ClickException, Choice
from click.exceptions import Exit, Abort
from loguru import logger

import floxcore
from floxcore.console import error_box
from floxcore.exceptions import FloxException

GLOBAL_OPTIONS = (
    click.core.Option(("-v",), default=False, is_flag=True, help="Verbose mode - show debug info"),
)


def append_unique(params: list, *options):
    existing = list(map(lambda x: x.name, params))
    for option in options:
        if option.name in existing:
            continue

        params.append(option)
        existing.append(option.name)


class FloxCommand(click.core.Command):

    def __init__(self, name, context_settings=None, callback=None, params=None, help=None, epilog=None, short_help=None,
                 options_metavar="[OPTIONS]", add_help_option=True, no_args_is_help=False, hidden=False,
                 deprecated=False, params_from=None, with_plugin_selector=False):
        super().__init__(name, context_settings, callback, params, help, epilog, short_help, options_metavar,
                         add_help_option, no_args_is_help, hidden, deprecated)
        self.with_plugin_selector = with_plugin_selector
        self.params_from = params_from or []

        self.params.extend(
            GLOBAL_OPTIONS
        )
        self.global_values = {}

    def invoke(self, ctx):
        state = {}
        if hasattr(self, "pre_invoke"):
            state = self.pre_invoke(ctx.obj)

        for opt in GLOBAL_OPTIONS:
            self.global_values[opt.name] = ctx.params.pop(opt.name, None)

        try:
            result = super().invoke(ctx)
        except (ClickException, Exit, Abort) as e:
            raise e
        except Exception as e:
            if floxcore.DEBUG:
                logger.exception(e)
            raise FloxException(str(e))
        finally:
            if hasattr(self, "post_invoke"):
                self.post_invoke(ctx.obj, pre_invoke_state=state)

        return result

    def get_params(self, ctx):
        for param_name in self.params_from:
            for plugin in ctx.obj.plugins.handlers(f"command_options_{param_name}").values():
                for command_name, kwargs in plugin.handle(f"command_options_{param_name}"):
                    append_unique(self.params, click.core.Option((command_name,), **kwargs))

        if self.with_plugin_selector:
            self._add_plugins(ctx)

        return super().get_params(ctx)

    def _add_plugins(self, ctx):
        if ctx.obj.initiated:
            active = ctx.obj.meta.features
            append_unique(
                self.params,
                click.core.Option(
                    (f"--scope",),
                    type=Choice(active),
                    show_choices=True,
                    multiple=True,
                    help="Execute stages only from given plugins",
                )
            )
        else:
            for name, plugin in ctx.obj.plugins.plugins.items():
                append_unique(
                    self.params,
                    click.core.Option(
                        (f"--with-{name}/--without-{name}",),
                        default=True,
                        is_flag=True,
                        help=plugin.description,
                    )
                )


click.core.Command = FloxCommand
click.decorators.Command = FloxCommand
click.Command = FloxCommand

ClickMultiCommand = type('MultiCommand', (FloxCommand,), dict(click.core.MultiCommand.__dict__))


class FloxMultiCommand(ClickMultiCommand):
    def __init__(
            self,
            name=None,
            invoke_without_command=False,
            no_args_is_help=None,
            subcommand_metavar=None,
            chain=False,
            result_callback=None,
            **attrs
    ):
        super().__init__(name, invoke_without_command, no_args_is_help, subcommand_metavar, chain, result_callback,
                         **attrs)


click.core.MultiCommand = FloxMultiCommand
click.MultiCommand = FloxMultiCommand

ClickGroup = type('Group', (click.core.MultiCommand,), dict(click.core.Group.__dict__))


class FloxGroup(ClickGroup):

    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)


click.core.Group = FloxGroup
click.decorators.Group = FloxGroup
click.Group = FloxGroup


def show(self):
    error_box(message=self.message)


click.ClickException.show = show

patched = True

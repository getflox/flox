from floxcore import FloxContext

from flox.project.workflow import apply_stages


def apply_settings(flox: FloxContext):
    stages = flox.project.stages

    apply_stages(flox, stages)

from os.path import abspath

import click
import git


def colourize(name):
    if name in ["prod", "production", "live"]:
        return click.style(name, fg="red")
    elif name in ["uat", "preprod", "test"]:
        return click.style(name, fg="yellow")
    elif name in ["staging", "integration"]:
        return click.style(name, fg="green")
    else:
        return name


def locate_project_root():
    try:
        git_repo = git.Repo(abspath(__file__), search_parent_directories=True)
        return git_repo.git.rev_parse("--show-toplevel")
    except Exception:
        return None

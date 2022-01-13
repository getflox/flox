# flox

Flox is an opinionated orchestration and automation tool for microservice development using modern stack.

With flox we aim to automate the boring parts of project creation letting you focus on your business logic.

Flox has a modular architecture, allowing you to extend its functionality with plugins.

Flox can:

- Create git repository (with [flox-git](https://github.com/getflox/flox-git))
- Create and configure GitHub repositories (with [flox-github](https://github.com/getflox/flox-github))
- Create sentry project and integrate it with your project (with [flox-sentry](https://github.com/getflox/flox-sentry))
- Bootstrap your project using your own templates (with [flox-bootstrap](https://github.com/getflox/flox-git))

Soon to see:

- AWS integration
- Terraform support
- Serverless support


## Key features

- Multi level configuration support (define system, user and project level configuration)
- Support for secrets with native system keyring support 
- Plugin architecture with build-in plugin manager
- Workflow support (automatically create branches, PR and more...)
- Support for multiple profiles (prod, dev... name it)
- Interactive configuration management based on the plugin requirements 
- Work in command line mode or in interactive shell

## Configuration

Flox supports hierarchical configuration with merging and overwriting support on each level, with possibility with 
custom configuration per profile. 

Current configuration load order:
* /etc/flox/settings.toml
* /etc/flox/settings.{profile}.toml
* ~/.flox/settings.toml
* ~/.flox/settings.{profile}.toml
* {project_root}/.flox/settings.toml
* {project_root}/.flox/settings.{profile}.toml

Global configuration of the flox system itself is defined under `global` section , while each plugin
has it's own dedicated section.  

Additionally flox supports interactive environment configuration with `flox configure` command.
Configuration command uses plugin autodiscvery, to list all available options run `flox configure --help`.


## Installation 

```bash
$ pip install flox-cli
```

optionally you can specify extra features to be installed at the same time:

```bash
$ pip install flox-cli[git,github,bootstrap,sentry]
```

```bash
$ flox --help
Usage: flox [OPTIONS] COMMAND [ARGS]...

  Consistent project management and automation with flox

Options:
  -v      Verbose mode - show debug info
  --help  Show this message and exit.

Commands:
  config   Run configuration wizard for flox.
  plugin   Manage plugins
  project  Initialise new project with flox
```

### Plugin management

List all installed plugins

```bash
$ flox plugin 

 name       description                                                                                url                                     version
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 global     Highly opinionated workflow and orchestration toolkit for modern microservice development  https://github.com/getflox/flox         0.5.0
 git        Bootstrap git repository for your project managed by flox.                                 https://github.com/getflox/flox-git     0.2.0
 github     Create and enforce standard rules on GitHub repositories managed by flox.                  https://github.com/getflox/flox-github  0.1.2
 bootstrap                                                                                             None                                    0.1.2
 sentry     Automatically create projects and teams for flox managed projects                          https://github.com/getflox/flox-sentry  0.1.2
```

Search and install flox plugin

```bash
flox plugin search aws
flox plugin install flox-aws
```

### Project creation

With flox you can quickly create a new project to work on - please remember that flox relays on the plugins, so 
you must first install and configure plugins to see the real power of flox.

Example below was executed with git, github, bootstrap and sentry plugins installed. 

```bash
$ flox project --templates python --templates serverless-python                                                                                                                                                                                                                                                    11:53:39
Enter project name: Flox Project
Enter project description: Sample project created with flox
✔ [github]  Created GitHub repository 'https://github.com/getflox/flox-project'
✔ [git]  Initialised git repository
✔ [git]  Added new remote origin with github.com/getflox/flox-project.git
✔ [git]  Created new master branch
✔ [git]  Switched to master branch
✔ [sentry]  Project "flox-project" created
Bootstraps project with given templates:  46%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                                                                                                                                          | 6/13
 → Python Version [3.8.12]:
 → Enable xray support [Y/n]:
ℹ [bootstrap]  Bootstrapping project using template: python
ℹ [bootstrap]  Bootstrapping project using template: serverless-python
✔ [github]  Vulnerability alerts: On
✔ [github]  Automated security fixes enabled
✔ [github]  Branch protection rules set for "master" branch.
✔ [git]  Created default .gitignore: flox-project/.flox/.gitignore
✔ [git]  Added flox meta files to git repository
✔ [git]  Added flox bootstrapped files to git repository
ℹ [git]  Skipping branch master as branch already exists
✔ [git]  Pushed to remote origin
✔ [git]  Created branch develop
✔ [sentry]  Assigned  teams to flox-project project
✔ [git]  Pushed to remote origin
Push changes to remote: 100%|

$ ls -la ./flox-project
drwxr-xr-x   4 me  staff  128 Jan 13 11:54 .flox
drwxr-xr-x  13 me  staff  416 Jan 13 11:54 .git
-rw-r--r--   1 me  staff    6 Jan 13 11:54 .python-version
-rw-r--r--   1 me  staff   14 Jan 13 11:54 README.md
drwxr-xr-x   3 me  staff   96 Jan 13 11:54 flox__project
-rw-r--r--   1 me  staff  424 Jan 13 11:54 package.json
-rw-r--r--   1 me  staff  454 Jan 13 11:54 pyproject.toml
-rw-r--r--   1 me  staff  510 Jan 13 11:54 serverless.yml.py
```

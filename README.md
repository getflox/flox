# flox

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
$ pip install pip install git+https://github.com/getflox/flox.git
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

Search and install flox plugin

```bash
flox plugin search aws
flox plugin install flox-aws
```
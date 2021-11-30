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

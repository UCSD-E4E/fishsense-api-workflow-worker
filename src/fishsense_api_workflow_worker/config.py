"""Dynaconf settings module."""

import os
from pathlib import Path

import validators
from dynaconf import Dynaconf, Validator

IS_DOCKER = os.environ.get("E4EFS_DOCKER", False)


def get_config_path() -> Path:
    """Get config path

    Returns:
        Path: Path to config directory
    """
    if IS_DOCKER:
        return Path("/e4efs/config")
    config_path = Path(".")
    return config_path


validators = [
    Validator("temporal.host", required=True, cast=str),
    Validator("temporal.port", required=True, cast=str, default=7233),
]

settings = Dynaconf(
    envvar_prefix="E4EFS",
    environments=False,
    settings_files=[
        (get_config_path() / "settings.toml").as_posix(),
        (get_config_path() / ".secrets.toml").as_posix(),
    ],
    merge_enabled=True,
    validators=validators,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

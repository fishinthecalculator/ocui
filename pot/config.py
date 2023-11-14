from pathlib import Path

import toml
from appdirs import AppDirs
from textual import log

from pot.utils import get_version

DEFAULT_CONFIG = {
    "oci": {"runtime": "docker"},
    "ui": {"refresh_timeout": 10}
}


def get_config_path() -> Path | None:
    dirs = AppDirs(appname="pot", version=get_version())

    for config_path in [
        Path(dirs.user_config_dir, "pot.toml").absolute(),
        Path(dirs.site_config_dir, "pot.toml").absolute()
    ]:
        if config_path and Path(config_path).exists():
            log.debug(f"Loading configuration from {config_path}")
            return config_path


def read_config_file(config_path: Path) -> dict | None:
    if config_path is not None:
        with open(config_path, "r") as fp:
            return toml.load(fp)
    else:
        return None


def validate_config(config: dict) -> dict | None:
    if "oci" in config and "runtime" in config["oci"]:
        if config["oci"]["runtime"] not in ["docker", "podman"]:
            log.error(f"Unsupported runtime: {config['oci']['runtime']}")
            return None
    if "ui" in config and "refresh_timeout" in config["ui"]:
        if config["ui"]["refresh_timeout"] <= 0:
            log.error(f"UI refresh timeout must be a positive integer: {config['ui']['refresh_timeout']}")
            return None
    return config


def get_config() -> dict:
    """
    Creates a configuration object. Configuration files are checked in this order:

      1. User configuration directory. On Linux that's `$XDG_CONFIG_HOME/pot/<pot-version>`;
      2. System configuration directory. On Linux that's the first element of
         `$XDG_CONFIG_DIRS` + `/pot/<pot-version>`.
      3. The default configuration hardcoded in the package.

    The first available configuration will be loaded.
    """
    config_path = get_config_path()
    config = read_config_file(config_path)
    if config is not None:
        valid_config = validate_config(config)
        if valid_config is None:
            raise RuntimeError(f"Invalid configuration: {config_path}")
        else:
            return { **DEFAULT_CONFIG, **valid_config }
    else:
        return DEFAULT_CONFIG

import importlib.resources
import time
from asyncio import sleep
from importlib.abc import Traversable

from pot.config import REFRESH_TIMEOUT

POT_RESOURCES = importlib.resources.files("pot") / "res"
POT_CSS = importlib.resources.files("pot") / "ui" / "base" / "css"


def read_resource(resource_ref: Traversable) -> str:
    with importlib.resources.as_file(resource_ref) as resource_path:
        with open(resource_path, "r") as fp:
            return fp.read()


def get_tcss_path(file_name: str) -> str:
    tcss_ref = POT_CSS / f"{file_name}.tcss"
    with importlib.resources.as_file(tcss_ref) as tcss_path:
        return str(tcss_path)


def get_logo() -> str:
    logo_ref = POT_RESOURCES / "logo.txt"
    return read_resource(logo_ref)


def get_version() -> str:
    version_ref = POT_RESOURCES / "VERSION"
    return read_resource(version_ref)


def get_egg() -> str:
    egg_ref = POT_RESOURCES / "egg"
    return read_resource(egg_ref)


def next_update(start: time) -> int:
    diff = time.time() - start
    if diff < REFRESH_TIMEOUT:
        return REFRESH_TIMEOUT - diff
    else:
        return 0


async def poll_command(compute_value):
    while True:
        start = time.time()
        value = await compute_value()
        yield value
        await sleep(next_update(start))

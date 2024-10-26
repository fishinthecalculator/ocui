import importlib.resources
from importlib.abc import Traversable

OCUI_RESOURCES = importlib.resources.files("ocui") / "res"
OCUI_CSS = importlib.resources.files("ocui") / "ui" / "base" / "css"


def read_resource(resource_ref: Traversable) -> str:
    with importlib.resources.as_file(resource_ref) as resource_path:
        with open(resource_path, "r") as fp:
            return fp.read()


def get_tcss_path(file_name: str) -> str:
    tcss_ref = OCUI_CSS / f"{file_name}.tcss"
    with importlib.resources.as_file(tcss_ref) as tcss_path:
        return str(tcss_path)


def get_logo() -> str:
    logo_ref = OCUI_RESOURCES / "logo.txt"
    return read_resource(logo_ref)


def get_egg() -> str:
    egg_ref = OCUI_RESOURCES / "egg"
    return read_resource(egg_ref)

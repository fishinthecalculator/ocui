from abc import ABC

from pot.config import get_config
from pot.oci.command.container import ContainerCommand
from pot.oci.command.image import ImageCommand


class Runtime(ABC):

    def __init__(self, entrypoint: str):
        self.entrypoint = entrypoint
        self.images = ImageCommand(entrypoint)
        self.containers = ContainerCommand(entrypoint)

    @classmethod
    def get_instance(cls, entrypoint: str | None = None):
        if entrypoint is None:
            entrypoint = get_config()["oci"]["runtime"]
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls(entrypoint)
        return cls._instance

    @classmethod
    def clear(cls):
        cls._instance = None


class DockerRuntime(Runtime):
    def __init__(self):
        super().__init__("docker")


class PodmanRuntime(Runtime):
    def __init__(self):
        super().__init__("podman")

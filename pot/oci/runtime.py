from abc import ABC

from pot.oci.command.container import ContainerCommand
from pot.oci.command.image import ImageCommand

SUPPORTED_RUNTIMES = ["docker", "podman"]


class Runtime(ABC):

    def __init__(self, entrypoint: str):
        if entrypoint not in SUPPORTED_RUNTIMES:
            raise ValueError(f"Unsupported OCI Runtime: {entrypoint}")
        self.entrypoint = entrypoint
        self.images = ImageCommand(entrypoint)
        self.containers = ContainerCommand(entrypoint)

    @classmethod
    def get_instance(cls, entrypoint: str | None = None):
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

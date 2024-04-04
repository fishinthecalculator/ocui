from abc import ABC

from ocui.config import get_config
from ocui.oci.command.container import ContainerCommand
from ocui.oci.command.image import ImageCommand
from ocui.oci.serialization import ObjectDeserializer
from ocui.oci.serialization.container import DockerContainerDeserializer, PodmanContainerDeserializer
from ocui.oci.serialization.image import DockerImageDeserializer, PodmanImageDeserializer
from ocui.oci.serialization.solver import resolve_deserializers


class Runtime(ABC):

    def __init__(self, entrypoint: str, image_deserializer: ObjectDeserializer, container_deserializer: ObjectDeserializer):
        self.entrypoint = entrypoint
        self.images = ImageCommand(image_deserializer, entrypoint)
        self.containers = ContainerCommand(container_deserializer, entrypoint)


    @classmethod
    def get_instance(cls, entrypoint: str | None = None):
        if entrypoint is None:
            entrypoint = get_config()["oci"]["runtime"]
            image_deserializer, container_deserializer = resolve_deserializers(entrypoint)
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls(entrypoint, image_deserializer, container_deserializer)
        return cls._instance

    @classmethod
    def clear(cls):
        cls._instance = None


class DockerRuntime(Runtime):
    def __init__(self):
        super().__init__("docker", DockerImageDeserializer(), DockerContainerDeserializer())


class PodmanRuntime(Runtime):
    def __init__(self):
        super().__init__("podman", PodmanImageDeserializer(), PodmanContainerDeserializer())

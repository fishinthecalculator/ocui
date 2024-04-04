from ocui.oci.serialization.container import DockerContainerDeserializer, PodmanContainerDeserializer
from ocui.oci.serialization.image import DockerImageDeserializer, PodmanImageDeserializer

def resolve_deserializers(entrypoint: str):
    if entrypoint == "podman":
        return PodmanImageDeserializer(), PodmanContainerDeserializer()
    else:
        return DockerImageDeserializer(), DockerContainerDeserializer()
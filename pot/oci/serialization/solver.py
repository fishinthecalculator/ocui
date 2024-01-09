from pot.oci.serialization.container import DockerContainerDeserializer, PodmanContainerDeserializer
from pot.oci.serialization.image import DockerImageDeserializer, PodmanImageDeserializer

def resolve_deserializers(entrypoint: str):
    if entrypoint == "podman":
        return PodmanImageDeserializer(), PodmanContainerDeserializer()
    else:
        return DockerImageDeserializer(), DockerContainerDeserializer()
from ocui.oci.dataclass.image import Image
from ocui.oci.serialization import ObjectDeserializer
from ocui.oci.serialization.utils import parse_datetime

class DockerImageDeserializer(ObjectDeserializer):
    def deserialize(self, dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = parse_datetime(created)
        return Image(
            repository=dict_object["Repository"],
            tag=dict_object["Tag"],
            image_id=dict_object["ID"],
            created=created,
            size=dict_object.get("Size", None)
        )

class PodmanImageDeserializer(ObjectDeserializer):
    def deserialize(self, dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = parse_datetime(created)
        return Image(
            repository=dict_object["repository"],
            tag=dict_object["tag"],
            image_id=dict_object["Id"],
            created=created,
            size=dict_object.get("Size", None)
        )
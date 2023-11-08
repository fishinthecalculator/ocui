from dataclasses import dataclass
from datetime import datetime

from pot.oci.dataclass import DATETIME_FORMAT_STRING


@dataclass
class Image:
    repository: str
    tag: str = "latest"
    image_id: str | None = None
    created: datetime | None = None
    size: str | None = None

    @staticmethod
    def from_dict(dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = datetime.strptime(created, DATETIME_FORMAT_STRING)
        return Image(
            repository=dict_object["Repository"],
            tag=dict_object.get("Tag", "latest"),
            image_id=dict_object.get("ID", None),
            created=created,
            size=dict_object.get("Size", None)
        )

    def get_key(self):
        return self.image_id

    def format_created(self) -> str:
        return self.created.strftime(DATETIME_FORMAT_STRING)

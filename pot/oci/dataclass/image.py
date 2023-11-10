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
            created = Image.parse_created(created)
        return Image(
            repository=dict_object["Repository"],
            tag=dict_object.get("Tag", "latest"),
            image_id=dict_object.get("ID", None),
            created=created,
            size=dict_object.get("Size", None)
        )

    @staticmethod
    def parse_created(created: str) -> datetime:
        return datetime.strptime(created, DATETIME_FORMAT_STRING)

    def format_created(self) -> str:
        return self.created.strftime(DATETIME_FORMAT_STRING)

    def format_reference(self) -> str:
        return f"{self.repository}:{self.tag}"

    def get_key(self) -> str:
        return self.format_reference()

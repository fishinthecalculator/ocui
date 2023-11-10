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
    def from_dict(dict_object: dict):
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
    def from_tuple(t: tuple, spec: list[str]):
        kwargs = {k: v for k, v in zip(spec, t)}
        if kwargs["created"]:
            kwargs["created"] = Image.parse_created(kwargs["created"])
        return Image(**kwargs)

    @staticmethod
    def parse_created(created: str) -> datetime:
        return datetime.strptime(created, DATETIME_FORMAT_STRING)

    def to_tuple(self, spec) -> tuple:
        return tuple(
            getattr(self, a)
            if a not in ["created"]
            else getattr(self, f"format_{a}")()
            for a in spec
        )

    def format_created(self) -> str:
        return self.created.strftime(DATETIME_FORMAT_STRING)

    def format_reference(self) -> str:
        return f"{self.repository}:{self.tag}"

    def get_key(self) -> str:
        return self.format_reference()

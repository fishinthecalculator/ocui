from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pot.oci.dataclass import DATETIME_FORMAT_STRING


class ContainerState(Enum):
    CREATED = "created"
    RUNNING = "running"
    RESTARTING = "restarting"
    EXITED = "exited"
    PAUSED = "paused"
    DEAD = "dead"


@dataclass
class Container:
    container_id: str
    command: str
    image_ref: str
    created: datetime
    state: ContainerState
    ports: list[str]
    name: str

    @staticmethod
    def from_dict(dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = Container.parse_created(created)
        ports = dict_object.get("Ports")
        if ports and ports is str:
            ports = list(ports)
        return Container(
            container_id=dict_object["ID"],
            command=dict_object["Command"],
            image_ref=dict_object["Image"],
            created=created,
            state=ContainerState(dict_object["State"]),
            ports=ports,
            name=dict_object.get("Names")
        )

    @staticmethod
    def format_list_of_strings(list_of_strings):
        return " ".join(list_of_strings)

    @staticmethod
    def parse_created(created: str) -> datetime:
        return datetime.strptime(created, DATETIME_FORMAT_STRING)

    def format_created(self) -> str:
        return self.created.strftime(DATETIME_FORMAT_STRING)

    def get_key(self):
        return self.container_id

    def format_ports(self):
        if self.ports is str:
            return self.ports
        return Container.format_list_of_strings(self.ports)

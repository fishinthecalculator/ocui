from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pot.oci.dataclass import DATETIME_FORMAT_STRING


class ContainerState(Enum):
    CREATED = "created"
    RUNNING = "running"
    RESTARTING = "restarting"
    STOPPING = "stopping"
    EXITED = "exited"
    PAUSED = "paused"
    DEAD = "dead"


@dataclass
class Container:
    container_id: str
    command: str
    image: str
    created: datetime
    state: ContainerState
    ports: list[str]
    name: str | list[str]
    mounts: list[str] | None = None

    @staticmethod
    def from_dict(dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = Container.parse_created(created)
        return Container(
            container_id=dict_object["ID"] if "ID" in dict_object.keys() else dict_object["Id"],
            command=dict_object["Command"],
            image=dict_object["Image"],
            created=created,
            state=Container.parse_state(dict_object["State"]),
            ports=Container.parse_ports(dict_object.get("Ports", [])),
            mounts=Container.parse_mounts(dict_object.get("Mounts", [])),
            name=dict_object.get("Names")
        )

    @staticmethod
    def format_list_of_strings(list_of_strings: list[str]) -> str:
        if not list_of_strings:
            return None
        return " ".join(list_of_strings)

    @staticmethod
    def _parse_list_of_strings(string: str) -> list[str]:
        if string:
            return string.split(" ")
        else:
            return []

    @staticmethod
    def parse_created(created: str) -> datetime:
        return datetime.strptime(created, DATETIME_FORMAT_STRING)

    @staticmethod
    def parse_mounts(mounts: str) -> ContainerState:
        return Container._parse_list_of_strings(mounts)

    @staticmethod
    def parse_ports(ports: str) -> ContainerState:
        return Container._parse_list_of_strings(ports)

    @staticmethod
    def parse_state(state: str) -> ContainerState:
        return ContainerState(state)

    def to_tuple(self, spec) -> tuple:
        return tuple(
            getattr(self, a)
            if a not in ["created", "mounts", "state", "ports"]
            else getattr(self, f"format_{a}")()
            for a in spec
        )

    def format_created(self) -> str:
        if self.created:
            return self.created.strftime(DATETIME_FORMAT_STRING)
        else:
            return ""

    def format_ports(self):
        return Container.format_list_of_strings(self.ports)

    def format_mounts(self):
        return Container.format_list_of_strings(self.mounts)

    def format_state(self):
        return self.state.value

    def get_key(self):
        return self.container_id

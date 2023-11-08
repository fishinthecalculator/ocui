from dataclasses import dataclass
from datetime import datetime

from pot.oci.dataclass import DATETIME_FORMAT_STRING


@dataclass
class Container:
    container_id: str
    command: str
    image_name: str
    created: datetime
    status: str
    ports: list[str]
    names: list[str]

    @staticmethod
    def from_dict(dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = Container.parse_created(created)
        ports = dict_object.get("Ports")
        if ports and ports is str:
            ports = list(ports)
        names = dict_object.get("Names")
        if names and names is str:
            names = list(names)
        return Container(
            container_id=dict_object["ID"],
            command=dict_object["Command"],
            image_name=dict_object["Image"],
            created=created,
            status=dict_object["Status"],
            ports=ports,
            names=names
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

    def format_names(self):
        if self.names is str:
            return self.names
        return Container.format_list_of_strings(self.names)

    def format_ports(self):
        if self.ports is str:
            return self.ports
        return Container.format_list_of_strings(self.ports)

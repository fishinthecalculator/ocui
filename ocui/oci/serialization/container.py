from ocui.oci.dataclass.container import Container, ContainerState
from ocui.oci.serialization import ObjectDeserializer
from ocui.oci.serialization.utils import parse_list_of_strings, parse_datetime

def parse_mounts(mounts: str) -> list[str]:
    return parse_list_of_strings(mounts)

def parse_ports(ports: str) -> list[str]:
    # [{'host_ip': '', 'container_port': 3000, 'host_port': 3000, 'range': 1, 'protocol': 'tcp'}]
    return [f"{p['host_port']}:{p['container_port']}/{p['protocol']}" for p in ports]

def parse_state(state: str) -> ContainerState:
    return ContainerState(state)

class PodmanContainerDeserializer(ObjectDeserializer):
    def deserialize(self, dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = parse_datetime(created)
        return Container(
            container_id=dict_object["Id"],
            command=dict_object["Command"],
            image=dict_object["Image"],
            created=created,
            state=parse_state(dict_object["State"]),
            ports=parse_ports(dict_object.get("Ports", [])),
            mounts=parse_mounts(dict_object.get("Mounts", [])),
            name=dict_object.get("Names")
        )


class DockerContainerDeserializer(ObjectDeserializer):
    def deserialize(self, dict_object):
        created = dict_object.get("CreatedAt", None)
        if created:
            created = parse_datetime(created)
        return Container(
            container_id=dict_object["ID"],
            command=dict_object["Command"],
            image=dict_object["Image"],
            created=created,
            state=parse_state(dict_object["State"]),
            ports=parse_list_of_strings(dict_object.get("Ports", [])),
            mounts=parse_mounts(dict_object.get("Mounts", [])),
            name=dict_object.get("Names")
        )
import datetime
from abc import ABC, abstractmethod

from ocui.oci.dataclass.container import Container
from ocui.oci.dataclass.image import Image


UI_DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S %z %Z"


class UIAdapter(ABC):
    @staticmethod
    def format_list_of_strings(list_of_strings: list[str], separator=" ") -> str:
        if not list_of_strings:
            return ""
        return separator.join(list_of_strings)

    @staticmethod
    def format_datetime(dtime: datetime) -> str:
        if dtime:
            return dtime.strftime(UI_DATETIME_FORMAT_STRING)
        else:
            return ""

    @abstractmethod
    def to_tuple(self, value, spec) -> tuple:
        pass

class ImageAdapter(UIAdapter):
    def to_tuple(self, image: Image, spec) -> tuple:
        return tuple(
            getattr(image, a)
            if a not in ["created"]
            else getattr(self, f"format_{a}")(getattr(image, a))
            for a in spec
        )

    def format_created(self, created):
        return self.format_datetime(created)


class ContainerAdapter(UIAdapter):
    def to_tuple(self, container: Container, spec) -> tuple:
        return tuple(
            getattr(container, a)
            if a not in ["created", "mounts", "state", "ports"]
            else getattr(self, f"format_{a}")(getattr(container, a))
            for a in spec
        )

    def format_created(self, created):
        return self.format_datetime(created)

    def format_ports(self, ports):
        return self.format_list_of_strings(ports)

    def format_mounts(self, mounts):
        return self.format_list_of_strings(mounts)

    def format_state(self, state):
        return state.value
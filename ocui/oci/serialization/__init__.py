from abc import ABC, abstractmethod


DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S %z %Z"


class ObjectDeserializer(ABC):
    @abstractmethod
    def deserialize(self, value):
        pass
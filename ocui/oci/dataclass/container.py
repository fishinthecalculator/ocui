from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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
    name: str
    mounts: list[str] | None = None

    def get_key(self):
        return self.container_id

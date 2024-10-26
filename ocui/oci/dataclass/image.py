from dataclasses import dataclass
from datetime import datetime

@dataclass
class Image:
    image_id: str
    repository: str
    tag: str = "latest"
    created: datetime | None = None
    size: str | None = None

    def format_reference(self) -> str:
        return f"{self.repository}:{self.tag}"

    def get_key(self) -> str:
        return self.image_id

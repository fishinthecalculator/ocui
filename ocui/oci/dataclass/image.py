from dataclasses import dataclass
from datetime import datetime

@dataclass
class Image:
    repository: str
    tag: str = "latest"
    image_id: str | None = None
    created: datetime | None = None
    size: str | None = None

    def format_reference(self) -> str:
        return f"{self.repository}:{self.tag}"

    def get_key(self) -> str:
        return self.format_reference()

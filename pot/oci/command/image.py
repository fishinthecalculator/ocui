from pot.oci.command import RuntimeCommand
from pot.oci.dataclass.image import Image


class ImageCommand(RuntimeCommand):
    def __init__(self, runtime_entrypoint: str):
        super().__init__(runtime_entrypoint, "image")

    async def ls(self) -> list[Image]:
        dict_list = await self._exec_json_string(["ls", "--format", "{{json . }}"])
        return [Image.from_dict(image_dict) for image_dict in dict_list]

    async def remove(self, image: Image) -> str | None:
        return await self._exec(["rm", "-f", image.image_id])

    async def pull(self, image: Image) -> str | None:
        return await self._exec(["pull", f"{image.repository}:{image.tag}"])

from asyncio import create_task

from ocui.oci.command import RuntimeCommand
from ocui.oci.dataclass.image import Image
from ocui.oci.serialization import ObjectDeserializer


class ImageCommand(RuntimeCommand):
    def __init__(self, parser: ObjectDeserializer, runtime_entrypoint: str):
        super().__init__(runtime_entrypoint, parser, "image")

    async def inspect(self, image: Image) -> dict:
        dict_list = await self._exec_json_list(["inspect", image.image_id, "--format", "{{ json . }}"])
        return dict_list[0]

    async def ls(self) -> list[Image]:
        dict_list = await self._exec_json_list(["ls", "--format", "{{json . }}"])
        return [self.parser.deserialize(image_dict) for image_dict in dict_list]

    async def remove(self, image: Image) -> None:
        create_task(self._exec_collect(["rm", "-f", image.image_id]))

    async def pull(self, image: Image) -> None:
        create_task(self._exec_collect(["pull", image.format_reference()]))

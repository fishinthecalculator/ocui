from pot.oci.command import RuntimeCommand
from pot.oci.dataclass.container import Container


class ContainerCommand(RuntimeCommand):
    def __init__(self, runtime_entrypoint: str):
        super().__init__(runtime_entrypoint, "container")

    async def inspect(self, container: Container) -> dict:
        dict_list = await self._exec_json_string(["inspect", container.container_id, "--format", "{{ json . }}"])
        return dict_list[0]

    async def ls(self) -> list[Container]:
        dict_list = await self._exec_json_string(["ls", "-a", "--format", "{{ json . }}"])
        return [Container.from_dict(container_dict) for container_dict in dict_list]

    async def remove(self, container: Container) -> None:
        await self._exec(["rm", "-f", container.container_id])

    async def start(self, container: Container) -> None:
        await self._exec(["inspect", container.container_id])

    async def stop(self, container: Container) -> None:
        await self._exec(["stop", container.container_id])

from asyncio import create_task
from asyncio.subprocess import Process

from ocui.oci.command import RuntimeCommand
from ocui.oci.dataclass.container import Container, ContainerState
from ocui.oci.serialization import ObjectDeserializer


class ContainerCommand(RuntimeCommand):
    def __init__(self, parser: ObjectDeserializer, runtime_entrypoint: str):
        super().__init__(runtime_entrypoint, parser, "container")

    async def inspect(self, container: Container) -> dict:
        dict_list = await self._exec_json_list(["inspect", container.container_id, "--format", "{{ json . }}"])
        return dict_list[0]

    async def log(self, container: Container) -> Process:
        follow_states = [ContainerState.RUNNING, ContainerState.CREATED, ContainerState.RESTARTING]
        args = ["-f"] if container.state in follow_states else []
        process = await self._exec(["logs", *args, container.container_id])
        return process

    async def ls(self) -> list[Container]:
        dict_list = await self._exec_json_list(["ls", "-a", "--format", "{{ json . }}"])
        return [self.parser.deserialize(container_dict) for container_dict in dict_list]

    async def run(self, image_ref: str, name: str | None = None, ports: list[str] | None = None, volumes: list[str] | None = None,  remove: bool = False) -> None:
        args = []
        if name:
            args += ["--name", name]
        if ports:
            for p in ports:
                args += ["-p", p]
        if volumes:
            for m in volumes:
                args += ["-v", m]
        create_task(self._exec_drop(["run", *args, image_ref]))

    async def remove(self, container: Container) -> None:
        create_task(self._exec_collect(["rm", "-f", container.container_id]))

    async def start(self, container: Container) -> None:
        create_task(self._exec_collect(["start", container.container_id]))

    async def stop(self, container: Container) -> None:
        create_task(self._exec_collect(["stop", container.container_id]))

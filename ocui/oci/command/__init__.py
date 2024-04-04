import asyncio
import json
from abc import ABC
from asyncio.subprocess import Process

from ocui.oci.serialization import ObjectDeserializer


class RuntimeCommand(ABC):

    def __init__(self, runtime_entrypoint: str, parser: ObjectDeserializer, name: str):
        self.runtime_entrypoint = runtime_entrypoint
        self.parser = parser
        self.name = name

    async def _exec(self, args: list[str], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL) -> Process:
        args = [self.name] + args
        return await asyncio.create_subprocess_exec(self.runtime_entrypoint, *args, stdout=stdout, stderr=stderr)

    async def _exec_drop(self, args: list[str]) -> None:
        process = await self._exec(args, stdout=asyncio.subprocess.DEVNULL)
        await process.wait()
        if process.returncode != 0:
            raise RuntimeError(
                f"{' '.join([self.runtime_entrypoint, *args])} failed with exit code: {process.returncode}")

    async def _exec_collect(self, args: list[str]) -> str | None:
        process = await self._exec(args)
        data, _ = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(
                f"{' '.join([self.runtime_entrypoint, *args])} failed with exit code: {process.returncode}")
        if data:
            return data.decode()
        else:
            return None

    async def _exec_json_list(self, args: list[str]) -> list[dict]:
        output = await self._exec_collect(args)
        if not output:
            return []
        else:
            return [
                json.loads(line) for line in output.strip().split("\n")
            ]

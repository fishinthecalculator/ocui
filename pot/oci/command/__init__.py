import asyncio
import json
from abc import ABC


class RuntimeCommand(ABC):

    def __init__(self, runtime_entrypoint: str, name: str):
        self.runtime_entrypoint = runtime_entrypoint
        self.name = name

    async def _exec(self, args: list[str]) -> str | None:
        args = [self.name] + args
        process = await asyncio.create_subprocess_exec(self.runtime_entrypoint, *args, stdout=asyncio.subprocess.PIPE)
        data, _ = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(
                f"{' '.join([self.runtime_entrypoint, *args])} failed with exit code: {process.returncode}")
        if data:
            return data.decode()
        else:
            return None

    async def _exec_json_string(self, args: list[str]) -> list[dict]:
        output = await self._exec(args)
        if not output:
            return []
        else:
            return [
                json.loads(line) for line in output.strip().split("\n")
            ]

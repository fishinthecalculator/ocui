import time
from asyncio import sleep

from ocui.config import get_config


def next_update(start: time) -> int:
    refresh_timeout = get_config()["ui"]["refresh_timeout"]
    diff = time.time() - start
    if diff < refresh_timeout:
        return refresh_timeout - diff
    else:
        return 0


async def poll_command(compute_value):
    while True:
        start = time.time()
        value = await compute_value()
        yield value
        await sleep(next_update(start))


async def stream_command(streaming_command):
    process = await streaming_command()
    while True:
        data = await process.stdout.readline()
        if data == b'':
            break
        yield data.decode().strip()

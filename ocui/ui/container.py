from textual import work
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import RichLog

from ocui.oci.dataclass.container import Container
from ocui.oci.runtime import Runtime
from ocui.ui.adapters import ContainerAdapter
from ocui.ui.base.screen import RefreshTableScreen, BaseScreen
from ocui.ui.base.utils import stream_command
from ocui.ui.inspect import InspectScreen
from ocui.ui.run import RunContainerScreen


class ContainerLogScreen(BaseScreen, ModalScreen):
    """A live log listing modal screen."""

    BINDINGS = [("q", "quit", "Quit"),
                ("escape", "app.pop_screen", "Back")]

    def __init__(self, container: Container):
        super().__init__(Runtime.get_instance(), f"{container.container_id}\\logs")
        self.rich_log = RichLog(id="rich_log")
        self.container = container

    def _follow_logs(self):
        return self.get_backend().containers.log(self.container)

    def _compose(self) -> ComposeResult:
        yield self.rich_log

    async def on_mount(self) -> None:
        self.refresh_screen()

    @work(exclusive=True)
    async def refresh_screen(self) -> None:
        """Update the current screen."""
        async for value in stream_command(self._follow_logs):
            self.rich_log.write(value)


class ContainersScreen(RefreshTableScreen):
    """A containers listing widget."""

    adapter = ContainerAdapter()

    BINDINGS = [
        ("i", "inspect", "Inspect"),
        ("d", "delete", "Delete"),
        ("r", "run", "Run container"),
        ("l", "log", "Show logs"),
        ("k", "stop", "Stop"),
        ("s", "start", "Start")
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance(), "containers")

    async def action_delete(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.remove(container)

    async def action_inspect(self):
        container = self.get_selection()
        if container:
            container_details = await self.get_backend().containers.inspect(container)
            await self.app.push_screen(InspectScreen(container.container_id, container_details))

    async def action_log(self):
        container = self.get_selection()
        if container:
            await self.app.push_screen(ContainerLogScreen(container))

    async def action_run(self):
        await self.app.push_screen(RunContainerScreen(self.get_backend()))

    async def action_start(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.start(container)

    async def action_stop(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.stop(container)

    def _get_columns(self):
        return ["container_id", "command", "image", "created", "state", "ports", "name"]

    async def _compute_value(self):
        return await self.get_backend().containers.ls()

    def _value_to_row(self, container: Container, spec: list[str]):
        return self.adapter.to_tuple(container, spec)

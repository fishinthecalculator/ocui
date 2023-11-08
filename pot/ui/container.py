from textual import work
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import RichLog

from pot.oci.dataclass.container import Container, ContainerState
from pot.oci.runtime import Runtime
from pot.ui.base.screen import RefreshTableScreen, BaseScreen
from pot.ui.base.utils import stream_command
from pot.ui.inspect import InspectScreen


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

    BINDINGS = [
        ("i", "inspect", "Inspect"),
        ("l", "log", "Show logs"),
        ("k", "stop", "Stop"),
        ("r", "remove", "Remove"),
        ("s", "start", "Start")
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance(), "containers")

    async def action_inspect(self):
        container = self.get_selection()
        if container:
            container_details = await self.get_backend().containers.inspect(container)
            await self.app.push_screen(InspectScreen(container.container_id, container_details))

    async def action_log(self):
        container = self.get_selection()
        if container:
            await self.app.push_screen(ContainerLogScreen(container))

    async def action_remove(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.remove(container)

    async def action_start(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.start(container)

    async def action_stop(self):
        container = self.get_selection()
        if container:
            await self.get_backend().containers.stop(container)

    def _get_columns(self):
        return ["container_id", "command", "image", "created", "state", "ports", "names"]

    async def _compute_value(self):
        return await self.get_backend().containers.ls()

    def _value_to_row(self, container: Container):
        return (container.container_id,
                container.command,
                container.image_name,
                container.format_created(),
                container.state.value,
                container.format_ports(),
                container.format_names())

    def _row_to_value(self, row):
        return Container(
            container_id=row[0],
            command=row[1],
            image_name=row[2],
            created=Container.parse_created(row[3]),
            state=ContainerState(row[4]),
            ports=row[5].split(" "),
            names=row[6].split(" "),
        )

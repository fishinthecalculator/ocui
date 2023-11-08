from pot.oci.dataclass.container import Container
from pot.oci.runtime import Runtime
from pot.ui.base.screen import RefreshTableScreen


class ContainersScreen(RefreshTableScreen):
    """A containers listing widget."""

    BINDINGS = [
        ("i", "inspect", "Inspect"),
        ("k", "stop", "Stop"),
        ("r", "remove", "Remove"),
        ("s", "start", "Start")
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance())

    async def action_inspect(self):
        await self.get_backend().containers.inspect()

    async def action_remove(self):
        container = self.get_selection()
        await self.get_backend().containers.remove(container)

    async def action_start(self):
        container = self.get_selection()
        await self.get_backend().containers.start(container)

    async def action_stop(self):
        container = self.get_selection()
        await self.get_backend().containers.stop(container)

    def _get_columns(self):
        return ["container_id", "command", "image", "created", "status", "ports", "names"]

    async def _compute_value(self):
        return await self.get_backend().containers.ls()

    def _value_to_row(self, container):
        return (container.container_id,
                container.command,
                container.image_name,
                container.format_created(),
                container.status,
                container.format_ports(),
                container.format_names())

    def _row_to_value(self, row):
        return Container(
            container_id=row[0],
            command=row[1],
            image_name=row[2],
            created=Container.parse_created(row[3]),
            status=row[4],
            ports=row[5].split(" "),
            names=row[6].split(" "),
        )

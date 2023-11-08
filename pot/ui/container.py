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
        selected_container_id = self.get_selection()
        await self.get_backend().containers.remove(selected_container_id)

    async def action_start(self):
        selected_container_id = self.get_selection()
        await self.get_backend().containers.start(selected_container_id)

    async def action_stop(self):
        selected_container_id = self.get_selection()
        await self.get_backend().containers.stop(selected_container_id)

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

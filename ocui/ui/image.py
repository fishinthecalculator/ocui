from ocui.oci.dataclass.image import Image
from ocui.oci.runtime import Runtime
from ocui.ui.adapters import ImageAdapter
from ocui.ui.base.screen import RefreshTableScreen
from ocui.ui.inspect import InspectScreen
from ocui.ui.run import RunContainerScreen


class ImagesScreen(RefreshTableScreen):
    """An images listing widget."""

    adapter = ImageAdapter()

    BINDINGS = [
        ("i", "inspect", "Inspect"),
        ("d", "delete", "Delete"),
        ("r", "run", "Run container"),
        ("p", "pull", "Pull")
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance(), "images")

    async def action_inspect(self):
        image = self.get_selection()
        if image:
            image_details = await self.get_backend().images.inspect(image)
            await self.app.push_screen(InspectScreen(image.repository, image_details))

    async def action_delete(self):
        image = self.get_selection()
        if image:
            await self.get_backend().images.remove(image)

    async def action_pull(self):
        image = self.get_selection()
        if image:
            await self.get_backend().images.pull(image)

    async def action_run(self):
        image = self.get_selection()
        if image:
            await self.app.push_screen(RunContainerScreen(self.get_backend(), image))

    def _get_columns(self):
        return ["image_id", "repository", "tag", "created", "size"]

    async def _compute_value(self):
        return await self.get_backend().images.ls()

    def _value_to_row(self, image: Image, spec: list[str]) -> tuple:
        return self.adapter.to_tuple(image, spec)


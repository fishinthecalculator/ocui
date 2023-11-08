from pot.oci.dataclass.image import Image
from pot.oci.runtime import Runtime
from pot.ui.base.screen import RefreshTableScreen
from pot.ui.inspect import InspectScreen


class ImagesScreen(RefreshTableScreen):
    """An images listing widget."""

    BINDINGS = [
        ("i", "inspect", "Inspect"),
        ("d", "remove", "Remove"),
        ("p", "pull", "Pull"),
        ("r", "run", "Run container")
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance(), "images")

    async def action_inspect(self):
        image = self.get_selection()
        if image:
            image_details = await self.get_backend().images.inspect(image)
            await self.app.push_screen(InspectScreen(image.repository, image_details))

    async def action_remove(self):
        image = self.get_selection()
        if image:
            await self.get_backend().images.remove(image)

    async def action_pull(self):
        image = self.get_selection()
        if image:
            await self.get_backend().images.pull(image)

    async def action_run(self):
        #image = self.get_selection()
        # if image:
            # await self.get_backend().images.remove(image)
        pass

    def _get_columns(self):
        return ["id", "repository", "tag", "created", "size"]

    async def _compute_value(self):
        return await self.get_backend().images.ls()

    def _value_to_row(self, image: Image):
        return (image.image_id,
                image.repository,
                image.tag,
                image.format_created(),
                image.size)

    def _row_to_value(self, row):
        return Image(
            image_id=row[0],
            repository=row[1],
            tag=row[2],
            created=Image.parse_created(row[3]),
            size=row[4]
        )

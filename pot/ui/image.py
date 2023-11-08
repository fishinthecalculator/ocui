from pot.oci.dataclass.image import Image
from pot.oci.runtime import Runtime
from pot.ui.base.screen import RefreshTableScreen


class ImagesScreen(RefreshTableScreen):
    """An images listing widget."""

    BINDINGS = [
        ("d", "remove", "Remove"),
    ]

    def __init__(self):
        super().__init__(Runtime.get_instance())

    async def action_remove(self):
        image = self.get_selection()
        await self.get_backend().images.remove(image)

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

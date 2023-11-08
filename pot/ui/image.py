from pot.oci.runtime import Runtime
from pot.ui.base.screen import RefreshTableScreen


class ImagesScreen(RefreshTableScreen):
    """An images listing widget."""

    def __init__(self):
        super().__init__(Runtime.get_instance())

    def _get_columns(self):
        return ["id", "repository", "tag", "created", "size"]

    async def _compute_value(self):
        return await self.get_backend().images.ls()

    def _value_to_row(self, image):
        return (image.image_id,
                image.repository,
                image.tag,
                image.format_created(),
                image.size)

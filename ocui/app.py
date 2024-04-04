from functools import partial

from textual.app import App
from textual.command import Provider, Hits, Hit

from ocui.config import init_logging, get_config, CONTAINERS_MODE, IMAGES_MODE, VOLUMES_MODE
from ocui.ui.container import ContainersScreen
from ocui.ui.image import ImagesScreen
from ocui.ui.volume import VolumesScreen
from ocui.utils import get_tcss_path


class ScreensCommands(Provider):
    """A command provider to change screens."""

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, OcuiApp)

        def build_hit(entity):
            command = f"open {entity}"
            return Hit(
                100,
                matcher.highlight(command),
                partial(lambda mode: app.switch_mode(mode), entity),
                help=f"Open the {entity} screen",
            )

        if matcher.match(CONTAINERS_MODE) > 0:
            yield build_hit(CONTAINERS_MODE)
        elif matcher.match(IMAGES_MODE) > 0:
            yield build_hit(IMAGES_MODE)
        elif matcher.match(VOLUMES_MODE) > 0:
            yield build_hit(VOLUMES_MODE)


class OcuiApp(App):
    """A Textual app to manage OCI containers."""

    COMMANDS = App.COMMANDS | {ScreensCommands}
    CSS_PATH = list(map(get_tcss_path, ["header", "body", "inspect"]))
    BINDINGS = [
        ("q", "quit", "Quit")
    ]
    MODES = {
        IMAGES_MODE: ImagesScreen,
        CONTAINERS_MODE: ContainersScreen,
        VOLUMES_MODE: VolumesScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode(get_config()["ui"]["startup_mode"])


def main():
    init_logging()
    app = OcuiApp()
    app.run()


if __name__ == '__main__':
    main()

from functools import partial

from textual.app import App
from textual.command import Provider, Hits, Hit

from pot.oci.runtime import Runtime
from pot.ui.container import ContainersScreen
from pot.ui.image import ImagesScreen
from pot.ui.volume import VolumesScreen
from pot.utils import get_tcss_path


class ScreensCommands(Provider):
    """A command provider to change screens."""

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, PotApp)

        def build_hit(entity):
            command = f"open {entity}"
            return Hit(
                100,
                matcher.highlight(command),
                partial(lambda mode: app.switch_mode(mode), entity),
                help=f"Open the {entity} screen",
            )

        if matcher.match("containers") > 0:
            yield build_hit("containers")
        elif matcher.match("images") > 0:
            yield build_hit("images")
        elif matcher.match("volumes") > 0:
            yield build_hit("volumes")


class PotApp(App):
    """A Textual app to manage OCI containers."""

    COMMANDS = App.COMMANDS | {ScreensCommands}
    CSS_PATH = list(map(get_tcss_path, ["header", "body"]))
    BINDINGS = [
        ("q", "quit", "Quit")
    ]
    MODES = {
        "images": ImagesScreen,
        "containers": ContainersScreen,
        "volumes": VolumesScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("containers")


def main():
    app = PotApp()
    Runtime.get_instance("docker")
    app.run()


if __name__ == '__main__':
    main()

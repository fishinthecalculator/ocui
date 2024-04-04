from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, Label

from ocui.ui.base.header import OcuiHeader


def render_dict(key: str, value: dict):
    layout = Vertical(id=key)
    layout.border_title = key
    with layout:
        for k, v in value.items():
            yield from render_item(k, v)


def render_item(key: str, value):
    if type(value) is dict:
        if len(value.keys()) > 0:
            yield from render_dict(key, value)
    else:
        stringified = str(value)
        if stringified:
            yield Label(f"{key}: {str(value)}")


class InspectScreen(ModalScreen):
    """A dynamic screen displaying the content of a dict."""

    BINDINGS = [("q", "quit", "Quit"),
                ("escape", "app.pop_screen", "Back")]

    def __init__(self, name: str, value: dict):
        super().__init__()
        self.value = value
        self.root = VerticalScroll(id="inspect_root")
        self.root.border_title = f"{name}\\details"

    def compose(self) -> ComposeResult:
        yield OcuiHeader()

        if len(self.value.keys()) > 0:
            with self.root:
                for k, v in self.value.items():
                    yield from render_item(k, v)

        yield Footer()

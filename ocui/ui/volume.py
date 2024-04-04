from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Placeholder


class VolumesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Placeholder("Volumes Screen")
        yield Footer()

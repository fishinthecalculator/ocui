import os

from textual.app import ComposeResult
from textual.widgets import Header, Static, Markdown

from ocui import __version__
from ocui.utils import get_logo


class OcuiHeader(Header):
    def __init__(self):
        super().__init__(show_clock=True)


class OcuiContext(Static):
    """The ocui context widget."""

    @staticmethod
    def _format_value(context: str, version: str, user: str):
        return f"""\
**context**: {context}

**version**: {version}

**user**:    {user}
        """

    def compose(self) -> ComposeResult:
        """Create child widgets of the context widget."""
        yield Markdown(
            OcuiContext._format_value("local", __version__, os.environ["USER"])
        )


class OcuiLogo(Static):
    """The ocui logo widget."""

    def __init__(self, *args, **kwargs):
        logo_txt = get_logo()
        super().__init__(logo_txt, *args, **kwargs)


class OcuiBar(Static):
    """The ocui context and logo bar widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of the bar."""
        yield OcuiContext(id="context")
        yield OcuiLogo(id="logo")

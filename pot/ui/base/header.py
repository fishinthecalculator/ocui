import os

from textual.app import ComposeResult
from textual.widgets import Header, Static, Markdown

from pot.utils import get_logo, get_version


class PotHeader(Header):
    def __init__(self):
        super().__init__(show_clock=True)


class PotContext(Static):
    """The pot context widget."""

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
            PotContext._format_value("local", get_version(), os.environ["USER"])
        )


class PotLogo(Static):
    """The pot logo widget."""

    def __init__(self, *args, **kwargs):
        logo_txt = get_logo()
        super().__init__(logo_txt, *args, **kwargs)


class PotBar(Static):
    """The pot context and logo bar widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of the bar."""
        yield PotContext(id="context")
        yield PotLogo(id="logo")

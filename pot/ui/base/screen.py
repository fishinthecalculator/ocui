from abc import ABC, abstractmethod, ABCMeta

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, DataTable

from pot.oci.runtime import Runtime
from pot.ui.base.header import PotHeader, PotBar
from pot.utils import poll_command


class MetaScreen(ABCMeta, type(Screen)):
    pass


class RefreshTableScreen(ABC, Screen, metaclass=MetaScreen):
    """A table listing widget."""
    def __init__(self, oci_backend: Runtime):
        super().__init__()
        self.table = DataTable()
        self.oci_backend = oci_backend

    @abstractmethod
    def _get_columns(self):
        pass

    @abstractmethod
    def _value_to_row(self, value):
        pass

    @abstractmethod
    async def _compute_value(self) -> list:
        pass

    def _add_rows(self, rows):
        for r in rows:
            row = self._value_to_row(r)
            self.table.add_row(*row, key=r.get_key())

    def get_backend(self):
        return self.oci_backend

    def get_selection(self) -> str:
        row_key, _ = self.table.coordinate_to_cell_key(self.table.cursor_coordinate)
        return row_key.value

    def compose(self) -> ComposeResult:
        yield PotHeader()
        yield PotBar()
        yield self.table
        yield Footer()

    async def on_mount(self) -> None:
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True
        self.table.add_columns(*self._get_columns())
        self._add_rows(await self._compute_value())

        self.refresh_screen()

    @work(exclusive=True)
    async def refresh_screen(self) -> None:
        """Update the weather for the given city."""
        async for value in poll_command(self._compute_value):
            self.table.clear()
            self._add_rows(value)

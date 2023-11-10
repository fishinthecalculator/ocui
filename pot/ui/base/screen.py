from abc import ABC, abstractmethod, ABCMeta

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, DataTable

from pot.oci.runtime import Runtime
from pot.ui.base.header import PotHeader, PotBar
from pot.ui.base.utils import poll_command


class MetaScreen(type(Screen), ABCMeta):
    pass


class BaseScreen(Screen, ABC, metaclass=MetaScreen):
    """The base pot screen."""
    def __init__(self, oci_backend: Runtime, container_title: str):
        super().__init__()
        self.oci_backend = oci_backend
        self.body = Vertical(id="container")
        self.body.border_title = container_title

    @abstractmethod
    def _compose(self):
        pass

    def get_backend(self):
        return self.oci_backend

    def get_body_title(self):
        return self.body.border_title

    def compose(self) -> ComposeResult:
        yield PotHeader()
        yield PotBar()
        with self.body:
            yield from self._compose()
        yield Footer()


class RefreshTableScreen(BaseScreen, ABC):
    """A table listing screen."""
    def __init__(self, oci_backend: Runtime, container_title: str):
        super().__init__(oci_backend, container_title)
        self.table = DataTable()

    @abstractmethod
    def _get_columns(self):
        pass

    @abstractmethod
    def _value_to_row(self, value, spec: list[str]):
        pass

    @abstractmethod
    def _row_to_value(self, row, spec: list[str]):
        pass

    @abstractmethod
    async def _compute_value(self) -> list:
        pass

    def _add_rows(self, rows):
        for r in rows:
            row = self._value_to_row(r, self._get_columns())
            self.table.add_row(*row, key=r.get_key())

    def _refresh_table(self, new_value):
        old_selection_index = self.table.cursor_coordinate.row
        self.table.clear()

        if new_value:
            self._add_rows(new_value)

            if old_selection_index > len(new_value):
                old_selection_index = len(new_value)

            self.table.move_cursor(row=old_selection_index)

    def get_selection(self):
        if self.table.row_count > 0:
            row_key, _ = self.table.coordinate_to_cell_key(self.table.cursor_coordinate)
            row = self.table.get_row(row_key)
            return self._row_to_value(row, self._get_columns())
        else:
            return None

    def _compose(self) -> ComposeResult:
        yield self.table

    async def on_mount(self) -> None:
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True
        self.table.add_columns(*self._get_columns())
        self._add_rows(await self._compute_value())

        self.refresh_screen()

    @work(exclusive=True)
    async def refresh_screen(self) -> None:
        """Update the table for the current screen."""
        async for value in poll_command(self._compute_value):
            self._refresh_table(value)

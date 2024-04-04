from abc import ABC, abstractmethod, ABCMeta

from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, DataTable

from ocui.oci.runtime import Runtime
from ocui.ui.base.header import OcuiHeader, OcuiBar
from ocui.ui.base.utils import poll_command


class MetaScreen(type(Screen), ABCMeta):
    pass


class BaseScreen(Screen, ABC, metaclass=MetaScreen):
    """The base ocui screen."""
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
        yield OcuiHeader()
        yield OcuiBar()
        with self.body:
            yield from self._compose()
        yield Footer()


class RefreshTableScreen(BaseScreen, ABC):
    """A table listing screen."""
    def __init__(self, oci_backend: Runtime, container_title: str):
        super().__init__(oci_backend, container_title)
        self.value = []
        self.table = DataTable()

    @abstractmethod
    def _get_columns(self):
        pass

    @abstractmethod
    def _value_to_row(self, value, spec: list[str]):
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
        self.value = new_value
        self.table.clear()

        if self.value:
            self._add_rows(self.value)

            if old_selection_index > len(self.value):
                old_selection_index = len(self.value)

            self.table.move_cursor(row=old_selection_index)

    def get_selection(self):
        if self.table.row_count > 0:
            return self.value[self.table.cursor_coordinate.row]
        else:
            return None

    def _compose(self) -> ComposeResult:
        yield self.table

    async def on_mount(self) -> None:
        self.table.cursor_type = "row"
        self.table.zebra_stripes = True
        self.table.add_columns(*self._get_columns())
        self.value = await self._compute_value()
        self._add_rows(self.value)

        self.refresh_screen()

    @work(exclusive=True)
    async def refresh_screen(self) -> None:
        """Update the table for the current screen."""
        async for value in poll_command(self._compute_value):
            self._refresh_table(value)

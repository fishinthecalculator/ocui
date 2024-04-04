from dataclasses import dataclass

from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Footer, Input, Label, Select

from ocui.config import CONTAINERS_MODE
from ocui.oci.dataclass.image import Image
from ocui.oci.runtime import Runtime
from ocui.ui.base.header import OcuiHeader

@dataclass
class RunContainerResult:
    image_ref: str
    remove: bool
    name: str | None = None
    ports: list[str] | None = None
    mounts: list[str] | None = None

class RunContainerScreen(ModalScreen):
    """A dynamic screen displaying the content of a dict."""

    BINDINGS = [("q", "quit", "Quit"),
                ("escape", "app.pop_screen", "Back")]

    def __init__(self, oci_runtime: Runtime, selected_image: Image | None = None):
        super().__init__()
        self.oci_runtime = oci_runtime
        self.root = VerticalScroll(id="run_container_root")
        select_args = [[]]
        select_kwargs = {"id": "image_select"}
        if selected_image:
            select_value = (selected_image.format_reference(), selected_image)
            select_args = [[select_value]]
            select_kwargs.update({"value": select_value})
        self.image_select = Select(*select_args, **select_kwargs)
        self.root.border_title = f"{selected_image.format_reference()}\\run" if selected_image else "run"
        self.rm_checkbox = Checkbox("Remove", id="rm_checkbox")
        self.ports_input = Input(id="ports_input", placeholder="3000, 443:443")
        self.volumes_input = Input(id="volumes_input", placeholder="/var/lib/grafana, /home:/opt/home")
        self.proceed_btn = Button("Proceed", id="proceed_button")

    def compose(self) -> ComposeResult:
        yield OcuiHeader()

        with Horizontal(id="top_row"):
            yield self.image_select
            yield self.rm_checkbox

        with Vertical(id="advanced"):
            yield Label("Ports")
            yield self.ports_input
            yield Label("Volumes")
            yield self.volumes_input

        yield self.proceed_btn

        yield Footer()

    def on_mount(self) -> None:
        self.fill_select()

    @work(exclusive=True)
    async def fill_select(self) -> None:
        self.image_select.set_options((i.format_reference(), i) for i in await self.oci_runtime.images.ls())

    def _get_result(self) -> RunContainerResult:
        return RunContainerResult(
            image_ref=self.image_select.value.format_reference(),
            remove=self.rm_checkbox.value,
            ports=self.ports_input.value.split(", ") if self.ports_input.value else [],
            mounts=self.volumes_input.value.split(", ") if self.volumes_input.value else []
        )

    @on(Button.Pressed)
    def validate_and_proceed(self, event: Button.Pressed) -> None:
        result = self._get_result()
        self.proceed(result)
        self.dismiss()
        self.app.switch_mode(CONTAINERS_MODE)

    @work(exclusive=True)
    async def proceed(self, result: RunContainerResult) -> None:
        await self.oci_runtime.containers.run(
            result.image_ref,
            ports=result.ports,
            volumes=result.mounts,
            remove=result.remove
        )
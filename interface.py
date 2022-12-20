from __future__ import annotations

from importlib_metadata import version
from pathlib import Path

from rich import box
from rich.console import RenderableType
from rich.json import JSON
from rich.markdown import Markdown
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive, watch
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Input,
    Static,
    TextLog,
)


MESSAGE = "TEST"

EXAMPLE_CSS = """\
Screen {
    layers: base overlay notes;
    overflow: hidden;
}
Sidebar {
    width: 40;
    background: $panel;
    transition: offset 500ms in_out_cubic;
    layer: overlay;
}
Sidebar.-hidden {
    offset-x: -100%;
}"""


class Sidebar(Container):

    def compose(self) -> ComposeResult:
        yield Title("")
        yield OptionGroup(Message(MESSAGE), Version())
        yield DarkSwitch()


class Version(Static):
    def render(self) -> RenderableType:
        return f"[b]v{version('textual')}"


class Title(Static):
    pass


class OptionGroup(Container):
    pass


class Message(Static):
    pass


class DarkSwitch(Horizontal):
    def compose(self) -> ComposeResult:
        yield Checkbox(value=self.app.dark)
        yield Static("Dark mode toggle", classes="label")

    def on_mount(self) -> None:
        watch(self.app, "dark", self.on_dark_change, init=False)

    def on_dark_change(self, dark: bool) -> None:
        self.query_one(Checkbox).value = self.app.dark

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        self.app.dark = event.value


def action_toggle_dark(self) -> None:
    self.dark = not self.dark


def action_toggle_sidebar(self) -> None:
    sidebar = self.query_one(Sidebar)
    self.set_focus(None)
    if sidebar.has_class("-hidden"):
        sidebar.remove_class("-hidden")
    else:
        if sidebar.query("*:focus"):
            self.screen.set_focus(None)
        sidebar.add_class("-hidden")


def test():
    pass


class InterfaceApp(App):

    CSS_PATH = "interface.css"
    TITLE = "Nodehex PDF Quality Tool"
    BINDINGS = [
        ("ctrl+b", "action_toggle_sidebar", "Sidebar"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True)
    ]

    show_sidebar = reactive(True)

    def compose(self) -> ComposeResult:
        example_css = "\n".join(
            Path(self.css_path[0]).read_text().splitlines()[:50])
        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=False),
            Footer()
        )


if __name__ == "__main__":
    app = InterfaceApp()
    app.run()

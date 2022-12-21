from __future__ import annotations

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

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
from textual.containers import Container, Horizontal, Vertical
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
    Label,
)

# Text blocks

MESSAGE = """

ASTRAEA is a suite of information management tools in development by Nodehex.

We are developing a series of free open source solutions to automate tasks, drive efficiency and leverage data in an effective manner within the Architecture, Engineering and Construction industry.

This tool will extract data from PDFs and provide a csv report output, requring less manual work from your information management teams.

You can find us on any of the links below. 

"""
LINK_GITHUB = """
    [@click="app.open_link('https://github.com/Eylas/')"]GITHUB[/]
    """
LINK_NODEHEX = """
    [@click="app.open_link('https://nodehex.com/')"]NODEHEX[/]
    """

# Container elements


class Sidebar(Container):

    def compose(self) -> ComposeResult:
        yield Title("about ASTRAEA")
        yield OptionGroup(Message(MESSAGE))
        yield Static(LINK_GITHUB, classes="SidebarLinks")
        yield Static(LINK_NODEHEX, classes="SidebarLinks")


class Options(Static):

    def compose(self) -> ComposeResult:
        yield Label("Select folder to review", classes="btnLabels")
        yield Button("Folder Location", id="event.button.folders")
        yield Label("Number of values to extract")
        yield Button("Select", classes="btnLabels")

# Button elements


class OptionGroup(Container):
    pass

# Text elements


class Message(Static):
    pass


class Title(Static):
    pass

# Actions


def askdirectory():
    dirname = filedialog.askdirectory()
    (f"Folder selected: {dirname}")
    return dirname

# App


class InterfaceApp(App):

    CSS_PATH = "interface.css"
    TITLE = "ASTRAEA"
    BINDINGS = [
        ("ctrl+b", "toggle_sidebar", "Sidebar"),
        ("ctrl+d", "toggle_dark", "Dark mode",),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True)
    ]

    show_sidebar = reactive(False)

    def add_note(self, renderable: RenderableType) -> None:
        self.query_one(TextLog).write(renderable)

    def compose(self) -> ComposeResult:
        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=False),
            Options(),
            TextLog()
        )
        yield Footer()

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser
        webbrowser.open(link)

    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one(Sidebar)
        self.set_focus(None)
        if sidebar.has_class("-hidden"):
            sidebar.remove_class("-hidden")
        else:
            if sidebar.query("*:focus"):
                self.screen.set_focus(None)
            sidebar.add_class("-hidden")

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:
        output = askdirectory()
        self.app.add_note(f"Folder selected: {output}")
        self.app.add_note(f"Type is {type(output)}")
        return output


if __name__ == "__main__":
    app = InterfaceApp()
    app.run()

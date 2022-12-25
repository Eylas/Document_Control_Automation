from __future__ import annotations

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import time

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
from rich.progress import track, Progress, BarColumn

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

# Data Table

# Text blocks

WELCOME_MD = """
Hey and welcome!

I developed this app with the aim of improving efficiency and saving time.

I hope it serves you will and if you have any questions - you can find me on the

"""
Welcome_var = Markdown(WELCOME_MD)

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


class Options(Container):

    def compose(self) -> ComposeResult:
        yield Button("Folder Location", id="event.button.folders")
        yield Button("Metadata upload", id="event.button.metadata")
        yield Button("Regex Patterns", id="event.button.regex")
        yield Input(placeholder="Enter Crop Location")
        yield Button("Extraction test")
        yield Button("Full extraction")
        yield Button("Save user settings")


class Progress(Container):
    def compose(self) -> ComposeResult:
        yield Static("Tracker", classes="trackers")
        yield Static("Tracker", classes="trackers")


class Metrics(Container):

    def compose(self) -> ComposeResult:
        yield Static("Number of files to process")
        yield Static("Someotherstuff")


class SavedTime(Container):

    def compose(self) -> ComposeResult:
        yield Static("Time", classes="trackers")
        yield Static("Time", classes="trackers")

# Button elements


class OptionGroup(Container):
    pass


# Text elements


class Message(Static):
    pass


class Title(Static):
    pass

# Actions


class Note_prefix(Static):
    prefix = "[#e3c404]NDX_Astraea:[/#e3c404] "


def askdirectory():
    dirname = filedialog.askdirectory()
    (f"Folder selected: {dirname}")
    return dirname

# Data Table

# Progress bars

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

    def add_note(self, renderable) -> None:
        self.query_one(TextLog).write(renderable)

    def compose(self) -> ComposeResult:
        yield Container(
            Sidebar(classes="-hidden"),
            Header(show_clock=False),
            Container(
                Vertical(
                    Title("Options"),
                    Options(id="options"),
                    id="left-pane",
                ),
                Container(
                    Metrics(),
                    Progress(),
                    SavedTime(),
                    id="top",
                ),
                TextLog(highlight=True, markup=True,
                        wrap=True),
                DataTable(),
                id="app-grid",
            ),
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

        if event.button.id == "event.button.folders":
            output = askdirectory()
            self.app.add_note(f"Folder selected: {output}")
            self.app.add_note(f"Type is {type(output)}")
            return output
        elif event.button.id == "event.button.metadata":
            self.app.add_note(f"{Note_prefix.prefix}metadata")
        else:
            self.app.add_note("Error")
            self.app.add_note(f"{Note_prefix.prefix}")

    def on_mount(self) -> None:
        self.add_note(
            f"{Note_prefix.prefix}Hey and welcome! Please refer to the documentation on how to use the application.\n")
        self.add_note(
            f"{Note_prefix.prefix}If you have any queries, please feel free to reach out to me if they're not covered in the documentation.\n")
        table = self.query_one(DataTable)
        table.add_column("Foo", width=20)
        table.add_column("Bar", width=20)
        table.add_column("Baz", width=20)
        table.add_column("Foo", width=20)
        table.add_column("Bar", width=20)
        table.add_column("Baz", width=20)
        table.zebra_stripes = True
        for n in range(20):
            table.add_row(*[f"Cell ([b]{n}[/b], {col})" for col in range(6)])


if __name__ == "__main__":
    app = InterfaceApp()
    app.run()

from lanman.screens.languages import LanguagesScreen
from textual.widgets import Footer
from rich.text import Text
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, OptionList

LINES = [
    "██╗      █████╗ ███╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗",
    "██║     ██╔══██╗████╗  ██║████╗ ████║██╔══██╗████╗  ██║",
    "██║     ███████║██╔██╗ ██║██╔████╔██║███████║██╔██╗ ██║",
    "██║     ██╔══██║██║╚██╗██║██║╚██╔╝██║██╔══██║██║╚██╗██║",
    "███████╗██║  ██║██║ ╚████║██║ ╚═╝ ██║██║  ██║██║ ╚████║",
    "╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝",
]
COLORS = ["#bb9af7", "#9d7cd8", "#7aa2f7", "#7dcfff", "#2ac3de", "#73daca"]
WIDTH = 56
OPTIONS = ["Languages", "Package Managers", "Install", "Quit"]


def title() -> Text:
    t = Text(no_wrap=True)
    for line, color in zip(LINES, COLORS):
        t.append(line + "\n", style=color)
    return t


class MenuScreen(Screen):
    DEFAULT_CSS = """
    MenuScreen { align: center middle; }
    #title { width: 56; height: auto; }
    #menu {
        width: 56;
        height: auto;
        margin-top: 2;
        border: none;
        background: transparent;
        padding: 0;
    }
    #menu > .option-list--option { padding: 0; }
    #menu > .option-list--option-highlighted {
        background: $accent;
        color: $text;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(title(), id="title")
        yield OptionList(*[o.center(WIDTH - 2) for o in OPTIONS], id="menu")
        yield Footer(show_command_palette=False)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        match event.option_index:
            case 0:
                self.app.push_screen(LanguagesScreen())
            case 3:
                self.app.exit()
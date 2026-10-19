from lanman.popups.password import PasswordPopUp
from lanman.screens.pac_man import PackageManagersScreen
from lanman.screens.languages import LanguagesScreen
import os
import sys
from pathlib import Path
from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, OptionList, Static
from lanman.version import download_update, install_binary, update_available

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

    BINDINGS = [Binding("q", "app.quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static(title(), id="title")
        yield OptionList(*[o.center(WIDTH - 2) for o in OPTIONS], id="menu")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.check_update()

    # ---- menu selection ----
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        match event.option_index:
            case 0:
                self.app.push_screen(LanguagesScreen())
            case 1:
                self.app.push_screen(PackageManagersScreen())
            case 3:
                self.app.exit()
            case 4:
                self.run_update()

    # ---- update check ----
    @work(thread=True)
    def check_update(self) -> None:
        new = update_available()
        if new:
            self.app.call_from_thread(self.add_update_option, new)

    def add_update_option(self, new: str) -> None:
        self.query_one("#menu", OptionList).add_option(
            f"⬆ Update to v{new}".center(WIDTH - 2)
        )

    # ---- update install ----
    @work(thread=True)
    def run_update(self) -> None:
        if not getattr(sys, "frozen", False):
            self.app.call_from_thread(
                self.app.notify, "Not running as the binary.", severity="warning"
            )
            return
        self.app.call_from_thread(self.app.notify, "Downloading update...")
        try:
            tmp = download_update()
        except Exception as e:
            self.app.call_from_thread(
                self.app.notify, str(e), title="Download failed", severity="error"
            )
            return
        self.app.call_from_thread(self.finish_update, tmp)

    def finish_update(self, tmp: Path) -> None:
        if os.access(Path(sys.executable).parent, os.W_OK):
            self.install(tmp, None)
        else:
            self.app.push_screen(PasswordPopUp(), lambda pw: self.install(tmp, pw))

    @work(thread=True)
    def install(self, tmp: Path, password: str | None) -> None:
        if password is None and not os.access(Path(sys.executable).parent, os.W_OK):
            tmp.unlink(missing_ok=True)
            return
        code = install_binary(tmp, password)
        tmp.unlink(missing_ok=True)
        if code == 0:
            self.app.call_from_thread(self.app.notify, "Updated. Restart LanMan.", timeout=10)
        else:
            self.app.call_from_thread(
                self.app.notify, "Install failed (wrong password?)", severity="error", timeout=10
            )
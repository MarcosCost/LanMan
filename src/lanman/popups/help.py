from textual.widgets import Markdown
from textual.containers import VerticalScroll
from textual.containers import ScrollableContainer
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Static


class HelpScreen(ModalScreen):
    BINDINGS = [("escape", "dismiss", "Close"), ("h", "dismiss", "Close")]

    DEFAULT_CSS = """
    HelpScreen { align: center middle; background: $background 60%; }
    #help {
        width: 60;
        height: auto;
        max-height: 80vh;
        padding: 0 1;
        border: round $accent;
        background: $surface;
    }
    #help_box { height: auto;max-height: 60vh; }
    #help_box Markdown {
        height: auto;
        margin: 0;
        padding: 0;
        background: transparent;
    }
    #help_box MarkdownH1 {
        text-align: left;
        margin: 0 0 1 0;
        padding: 0;
        background: transparent;
    }
    """

    HELP = """\
# LanMan

A TUI for managing programming languages and package managers on your machine.

## Menu

- **Languages**: scans your system for installed languages and shows their versions
- **Package Managers**: scans for installed package managers (pip, npm, cargo, etc.)
- **Install**: install a language or package manager
- **Quit**: exit LanMan

## Keys

- `↑` / `↓`: move through the menu
- `Enter`: select the highlighted option
- `h`: open this help
- `Esc`: close this help or go back
- `q`: quit

## Tips

- Scans can take a few seconds the first time.
- Scroll this window with the mouse or arrow keys if it doesn't fit.
"""

    def compose(self) -> ComposeResult:
        with Vertical(id="help"):
            yield VerticalScroll(Markdown(self.HELP), id="help_box")
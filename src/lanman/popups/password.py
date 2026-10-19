from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Static


class PasswordPopUp(ModalScreen[str | None]):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]

    DEFAULT_CSS = """
    PasswordPopUp { align: center middle; background: $background 60%; }
    #pw {
        width: 50;
        height: auto;
        padding: 1 2;
        border: round $accent;
        background: $surface;
    }
    #pw Static { width: 100%; height: auto; text-align: center; }
    #pw Input { width: 100%; }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="pw"):
            yield Static("[b]Password required[/b]")
            yield Static("sudo is needed to replace the binary.\n")
            yield Input(password=True, placeholder="sudo password")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)
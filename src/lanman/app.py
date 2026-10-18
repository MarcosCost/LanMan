from lanman.popups.help import HelpScreen
from textual.binding import Binding
from textual.app import App
from lanman.screens.menu import MenuScreen


class LanmanApp(App):
    BINDINGS = [
        Binding("q", "app.quit", "quit"),
        Binding("h", "help", "help"),
        Binding("ctrl+q", "app.noop", show=False)
    ]

    def action_help(self) -> None:
        if not isinstance(self.screen, HelpScreen):
            self.push_screen(HelpScreen())

    def on_mount(self) -> None:
        self.theme = "tokyo-night"
        self.push_screen(MenuScreen())

def main():
    LanmanApp().run()
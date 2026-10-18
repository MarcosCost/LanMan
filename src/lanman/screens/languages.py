import os
import subprocess
from pathlib import Path

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static, Tree

LANGUAGES = {
    "Python": ["python3", "python"],
    "JavaScript": ["node", "deno", "bun"],
    "TypeScript": ["tsc"],
    "Rust": ["rustc"],
    "Go": ["go"],
    "C": ["gcc", "clang", "tcc"],
    "C++": ["g++", "clang++"],
    "Java": ["java", "javac"],
    "Kotlin": ["kotlinc"],
    "Ruby": ["ruby"],
    "PHP": ["php"],
    "Lua": ["lua", "luajit"],
    "Perl": ["perl"],
    "Swift": ["swiftc", "swift"],
    "Dart": ["dart"],
    "Zig": ["zig"],
    "Haskell": ["ghc"],
    "Elixir": ["elixir"],
    "Julia": ["julia"],
    "R": ["Rscript"],
    ".NET": ["dotnet"],
}
VERSION_ARGS = {"go": "version", "swift": "--version"}


def find_all(name: str) -> list[Path]:
    """Every executable called `name` across PATH (not just the first)."""
    seen, found = set(), []
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = Path(d) / name
        if p.is_file() and os.access(p, os.X_OK):
            real = p.resolve()
            if real not in seen:
                seen.add(real)
                found.append(p)
    return found


def get_version(path: Path) -> str:
    arg = VERSION_ARGS.get(path.name, "--version")
    try:
        r = subprocess.run([str(path), arg], capture_output=True, text=True, timeout=3)
        out = (r.stdout or r.stderr).strip()
        return out.splitlines()[0] if out else "?"
    except Exception:
        return "?"


def scan() -> dict[str, list[tuple[Path, str]]]:
    result = {}
    for lang, bins in LANGUAGES.items():
        installs = [(p, get_version(p)) for b in bins for p in find_all(b)]
        if installs:
            result[lang] = installs
    return result


class LanguagesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    DEFAULT_CSS = """
    LanguagesScreen #tree { height: 1fr; margin: 1 2 0 2; border: round $accent; }
    LanguagesScreen #detail { height: 4; margin: 0 2 1 2; padding: 0 1; border: round $primary; }
    """

    TITLE = "Languages"

    def compose(self) -> ComposeResult:
        yield Header(icon='')
        yield Tree("Languages", id="tree")
        yield Static("Scanning...", id="detail")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        tree = self.query_one("#tree", Tree)
        tree.show_root = False
        tree.root.expand()
        self.run_scan()

    @work(thread=True)
    def run_scan(self) -> None:
        data = scan()
        self.app.call_from_thread(self.populate, data)

    def populate(self, data: dict) -> None:
        tree = self.query_one("#tree", Tree)
        for lang, installs in data.items():
            node = tree.root.add(f"[b]{lang}[/b] [dim]({len(installs)})[/dim]", expand=True)
            for path, version in installs:
                node.add_leaf(f"{path.name}  [dim]{version}[/dim]", data=path)
        self.query_one("#detail", Static).update(
            f"{len(data)} languages found. Select an entry to see its location."
        )
        tree.focus()

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        path = event.node.data
        detail = self.query_one("#detail", Static)
        if path is None:
            return
        real = path.resolve()
        text = f"[b]Path:[/b] {path}"
        if real != path:
            text += f"\n[b]Resolves to:[/b] {real}"
        detail.update(text)
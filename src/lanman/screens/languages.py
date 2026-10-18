import shutil
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

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

found = {
    lang: path
    for lang, bins in LANGUAGES.items()
    if (path := next((p for b in bins if (p := shutil.which(b))), None))
}

class LanguagesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Footer(show_command_palette=False)

    
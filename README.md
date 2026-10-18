# LanMan

A terminal UI for seeing which programming languages and language package managers are installed on your machine, where they live, and what versions you have.

Built with [Textual](https://textual.textualize.io/).

## Features

- **Languages**: scans `PATH` for installed languages (Python, Node, Rust, Go, Java, etc.)
- **Package Managers**: scans for language package managers (pip, uv, npm, cargo, gem, etc.)
- Lists every installation found across `PATH`, not just the first
- Shows version and resolved path (including symlink targets) for each entry
- Themes, help popup, keyboard-driven navigation

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Run

```
git clone git@github.com:MarcosCost/LanMan.git
cd LanMan
uv run lanman
```

## Install\

```
uv tool install .
```

Or editable, for development:

```
uv tool install -e .
```

Then run `lanman` from anywhere.

## Keys

| Key | Action |
|---|---|
| `↑` / `↓` | Move through menus and trees |
| `Enter` | Select |
| `Esc` | Go back / close popup |
| `h` | Help |
| `t` | Change theme |
| `q` | Quit (main menu) |

## Project layout

```
src/lanman/
├── __init__.py
├── app.py
├── screens/
|   ├── menu.py
|   ├── languages.py
|   └── package_managers.py
└── popups/
```


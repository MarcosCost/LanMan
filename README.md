# LanMan 0.1.1
A terminal UI for seeing which programming languages and language package managers are installed on your machine, where they live, and what versions you have.

Built with [Textual](https://textual.textualize.io/).

## Features

- **Languages**: scans `PATH` for installed languages (Python, Node, Rust, Go, Java, etc.)
- **Package Managers**: scans for language package managers (pip, uv, npm, cargo, gem, etc.)
- Lists every installation found across `PATH`, not just the first
- Shows version and resolved path (including symlink targets) for each entry
- Automatically notifies when github has been updated
- Themes

## Install

Linux only.Download the latest binary (no Python or uv needed):

```
curl -L -o lanman https://github.com/MarcosCost/LanMan/releases/latest/download/lanman-linux
chmod +x lanman && sudo mv lanman /usr/local/bin/
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

## Development

Requirements: Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```
git clone https://github.com/MarcosCost/LanMan
cd LanMan
uv run lanman
```

Install it as a command from source (editable):

```
uv tool install -e .
```

## Project layout

```
src/lanman/
├── __init__.py
├── app.py
├── screens/
|   ├── menu.py
|   ├── languages.py
|   └── pac_man.py
└── popups/
    └── help.py
```

# Next Planned features:

- Language and tool Installer
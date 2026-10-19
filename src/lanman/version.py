import json
import os
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from urllib.request import Request, urlopen

REPO = "MarcosCost/LanMan"
ASSET_URL = f"https://github.com/{REPO}/releases/latest/download/lanman-linux"


def _parse(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.lstrip("v").split("."))


def update_available() -> str | None:
    """Return the newer version string, or None if up to date / unknown."""
    try:
        req = Request(
            f"https://api.github.com/repos/{REPO}/releases/latest",
            headers={"User-Agent": "lanman"},
        )
        with urlopen(req, timeout=3) as r:
            latest = json.load(r)["tag_name"]
        if _parse(latest) > _parse(version("lanman")):
            return latest.lstrip("v")
    except Exception:
        pass
    return None


def download_update() -> Path:
    fd, name = tempfile.mkstemp(prefix="lanman-")
    os.close(fd)
    with urlopen(ASSET_URL, timeout=30) as r, open(name, "wb") as f:
        shutil.copyfileobj(r, f)
    return Path(name)


def install_binary(tmp: Path, password: str | None = None) -> int:
    cmd = ["install", "-m", "755", str(tmp), sys.executable]
    if password is None:
        return subprocess.run(cmd).returncode
    r = subprocess.run(
        ["sudo", "-S", "-k", "-p", ""] + cmd,
        input=password + "\n",
        text=True,
        capture_output=True,
    )
    return r.returncode
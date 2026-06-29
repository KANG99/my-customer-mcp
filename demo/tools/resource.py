"""Expose a local markdown file as an MCP Resource."""

import os
from pathlib import Path

_RESUME_DIR = os.path.join(Path(__file__).parent.parent, "poem")

async def read_poem() -> str:
    """Read the poem markdown file and return its content."""
    path = os.path.join(_RESUME_DIR, "黄金叹.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

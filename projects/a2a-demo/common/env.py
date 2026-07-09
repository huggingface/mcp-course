"""
Load `.env` from the project root, once, as an import side effect.

Importing this module (`import common.env`) picks up credentials like
XWEATHER_CLIENT_ID / XWEATHER_CLIENT_SECRET without requiring `export` in
the shell first. Only agent entrypoints need to import it - MCP servers are
launched as subprocesses that inherit the parent process's environment, so
whatever the agent loaded is already there by the time the MCP server reads
`os.environ`.
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

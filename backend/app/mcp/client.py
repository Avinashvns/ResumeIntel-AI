import os
import sys
from pathlib import Path

from mcp import (
    Client,
    StdioServerParameters,
)
from mcp.client.stdio import stdio_client


BACKEND_DIR = (
    Path(__file__).resolve().parents[2]
)

SERVER_PATH = (
    BACKEND_DIR
    / "app"
    / "mcp"
    / "server.py"
)


def get_server_parameters() -> StdioServerParameters:
    """
    Create the configuration used to launch
    the ResumeIntel MCP server.
    """

    python_path = os.pathsep.join(
        [
            str(BACKEND_DIR),
            os.environ.get(
                "PYTHONPATH",
                "",
            ),
        ]
    )

    return StdioServerParameters(
        command=sys.executable,
        args=[
            str(SERVER_PATH),
        ],
        cwd=str(BACKEND_DIR),
        env={
            **os.environ,
            "PYTHONPATH": python_path,
        },
    )


async def call_mcp_tool(
    tool_name: str,
    arguments: dict,
):
    """
    Launch the ResumeIntel MCP server over stdio,
    connect with an MCP client, and call an MCP tool.
    """

    server_parameters = (
        get_server_parameters()
    )

    async with Client(
        stdio_client(server_parameters)
    ) as client:

        return await client.call_tool(
            tool_name,
            arguments,
        )
from mcp.server import MCPServer


mcp = MCPServer(
    "ResumeIntel MCP Server"
)


@mcp.tool()
def health_check() -> str:
    """
    Check whether the ResumeIntel MCP server
    is running.
    """

    return "ResumeIntel MCP Server is healthy"


if __name__ == "__main__":
    mcp.run()
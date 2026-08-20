from app.mcp.server import mcp


def test_mcp_server_created() -> None:
    assert mcp is not None
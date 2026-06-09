# fastAPI < flask와 비슷
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello, World!")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
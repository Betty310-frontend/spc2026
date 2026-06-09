# fastAPI < flask와 비슷

import sys
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Hello, World!")

@mcp.tool()
def hello(name: str) -> str:
    print(f"[SERVER] hello 함수 호출됨: name={name}", file=sys.stderr)
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(f"[SERVER] 서버 시작", file=sys.stderr)
    mcp.run()
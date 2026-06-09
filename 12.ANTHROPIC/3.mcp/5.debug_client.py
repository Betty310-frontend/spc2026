import asyncio
from os import name
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python", args=["debug_proxy.py", "4.debug_server.py"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print(f"[CLIENT] 서버와 HS 전", file=sys.stderr)
            # 아래 코드를 통해 서버/클라 간에 handshake 이루어짐
            await session.initialize()
            print(f"[CLIENT] 서버와 HS 후", file=sys.stderr)

            tools = (await session.list_tools()).tools
            print(f"[CLIENT] 서버가 쓸 수 있는 도구 받아옴. 도구: {[t.name for t in tools]}")
            # 여기서부터 실제로 내가 서버에 호출하고 싶은 코드를 작성
            result = await session.call_tool("hello", {"name": "John"})
            print(result.content[0].text) # Hello, John!

if __name__ == "__main__":
    print(f"[CLIENT] 클라이언트 시작", file=sys.stderr)
    asyncio.run(main())
                                                       
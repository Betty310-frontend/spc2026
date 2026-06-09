import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "http://localhost:8000/mcp"

async def main():
    async with streamable_http_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 내가 원하는 코드는 여기서부터 시작
            tools = (await session.list_tools()).tools
            print(f"도구: {[t.name for t in tools]}")

            result = (await session.call_tool("now")).content[0].text
            print(f"현재 시간: {result}")

            

if __name__ == "__main__":
    asyncio.run(main())
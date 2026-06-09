import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["6.mcp_server_more_tools.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 너 어떤 도구를 가지고 있어?
            tools = (await session.list_tools()).tools
            print(f"도구: {[t.name for t in tools]}")

            result = (await session.call_tool("add", {"a": 5, "b": 3})).content[0].text
            print(f"add(5, 3) = {result}")    

            result = (await session.call_tool("word_count", {"text": "너는 어떤 서버니?"})).content[0].text
            print(f"word_count('너는 어떤 서버니?') = {result}")


if __name__ == '__main__':
    asyncio.run(main())
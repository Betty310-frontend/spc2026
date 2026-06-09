# pip install mcp
import mcp
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession

from importlib.metadata import version
import inspect

print(f"MCP version: {version('mcp')}")

print(f"\nMCP 문서\n{'-' * 50}")
print(inspect.getdoc(FastMCP))

print(f"\nMCP SSE App 문서\n{'-' * 50}")
print(inspect.getdoc(FastMCP.sse_app))

print(f"\nMCP 세션 관리 문서\n{'-' * 50}")
print(inspect.getdoc(ClientSession))
print(inspect.getdoc(ClientSession.initialize))
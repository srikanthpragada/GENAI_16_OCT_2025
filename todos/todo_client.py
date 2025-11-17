from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import asyncio

# Basic connection
transport = StreamableHttpTransport(url="http://127.0.0.1:9999/mcp")
client = Client(transport)

async def add_todo():
    async with client:
        # Call add
        result = await client.call_tool("add_todo", {"todo": 'First task'})
        print(result)
 

async def list_todos_by_importance(importance):
    async with client:
        # Call add
        result = await client.call_tool("todos_by_importance", {"importance": importance})
        print(result)

asyncio.run(list_todos_by_importance('high'))

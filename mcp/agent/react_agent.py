from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import asyncio

clients = MultiServerMCPClient(
    {"Number Server": {
        "url": "http://localhost:9999/mcp",
        "transport": "streamable_http"},
     "File Server:": {
        "command": "python",
        "args": ["./file_server.py"],
        "transport": "stdio"
    }
    }
)


async def process():
    tools = await clients.get_tools()
    model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    agent = create_agent(model, tools)
    prime_response = await agent.ainvoke({"messages": "is 383843 a prime number?"})
    print(prime_response["messages"][-1].content)

    perfect_response = await agent.ainvoke({"messages": "is 28 a prefect number?"})
    print(perfect_response["messages"][-1].content)

    file_response = await agent.ainvoke({"messages": "Get contents of test.txt file"})
    print(file_response["messages"][-1].content)

asyncio.run(process())

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

# Get key from environment variable
tavily_key = os.getenv("TAVILY_API_KEY")


clients = MultiServerMCPClient({"Tavily": {
    "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_key}",
    "transport": "streamable_http"}
})

async def process():
        tools = await clients.get_tools()
        model = init_chat_model("gpt-4o-mini", model_provider="openai")
        #model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
        agent = create_agent(model, tools)
        response = await agent.ainvoke({"messages": "Who won IPL 2025?"})
        print(response["messages"][-1].content)


asyncio.run(process())

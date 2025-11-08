# Program to show how LLM can call a tool based on the requirement
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage, AIMessage
import requests

@tool
def get_weather(latitude, longitude):
    """function to return weather information based on latitude and longitude"""

    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    data = response.json()
    return data["current_weather"]


@tool
def get_coordinates(city_name):
    """Return latitude & longitude for a city"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    first = data["results"][0]
    return {"latitude": first["latitude"], "longitude": first["longitude"]}


gemini = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0
)


system_message = SystemMessage(
    "You are a helpful weather assistant.If needed, find out latitude and logitude then provide to tool. ")
user_message = HumanMessage("What is the weather in Perth")

messages = [
    system_message,
    user_message
]

gemini_with_tools = gemini.bind_tools([get_coordinates, get_weather])

for step in range(5):
    response = gemini_with_tools.invoke(messages)
    messages.append(response)

    if len(response.tool_calls) > 0:
        for tool_call in response.tool_calls:
            func_name = tool_call["name"]
            tool_call_id = tool_call['id']
            tool = eval(func_name)

            # Call the tool and add result
            tool_result = tool.invoke(tool_call)

            tool_message = ToolMessage(
                content = tool_result,
                tool_call_id = tool_call_id
            )

            messages.append(tool_message)
    else:
        break 


for message in messages:
    message.pretty_print()
  
 

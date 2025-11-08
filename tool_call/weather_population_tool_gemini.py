from langchain.chat_models import init_chat_model
from langchain_core.tools import tool 
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage

@tool
def get_weather(location: str) -> str:
    """ 
    Gets weather in the given location
    """
    return "Sunny with 31C"

@tool 
def get_population(location: str) -> str:
    """
    Gets population in the given location
    """
    return "1 million."


gemini = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0
)

user_message = HumanMessage(content = "What is the weather in Vizag and its population")

gemini_with_tools = gemini.bind_tools ([get_weather, get_population])
response = gemini_with_tools.invoke([user_message])
 
# It only tells which tool is to be invoked to get the result. And 
# it does NOT call the tool itself

messages = [user_message, response]

for message in messages:
    message.pretty_print()

for tool in response.tool_calls:    
    chosen_function_name =  tool["name"]
    chosen_function = eval(chosen_function_name)
    tool_call_id = tool['id']
    #Call the function and put result as Tool Message 
    function_result = chosen_function.invoke(tool)

    messages.append( 
        ToolMessage(content=function_result,  tool_call_id=tool_call_id)
    )


final_result = gemini_with_tools.invoke(messages)
messages.append(final_result)
 

for message in messages:
    message.pretty_print()

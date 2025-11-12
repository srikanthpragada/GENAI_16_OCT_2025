import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langsmith-demo"

import langsmith
from langgraph.types import interrupt, Command
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from langgraph.prebuilt import tools_condition, ToolNode


# %%
print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Project:", os.getenv("LANGCHAIN_PROJECT"))
print("API key present:", bool(os.getenv("LANGCHAIN_API_KEY")))

# %%

# %%


class State(MessagesState):
    age: int
    name: str

# %%


def process(state: State):
    """ Process admission based on age. """
    print("Process tool called!")

    if state['age'] < 18:
       approval = interrupt(
           f"Do you want to approve the admission of {state['age']} years old?")
       if approval:
           print("Processed the admission of a minor!")
           return state
    else:
      print("Processed Major's Admission")
      return state


# %%
tools = [process]

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
llm_with_tools = llm.bind_tools(tools)

# %%
# System message
sys_msg = SystemMessage(content="You are a helpful assistant.")

# Node


def call_llm(state: State):
    result = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [result], "state": state}


# %%
# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("call_llm", call_llm)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine the control flow
builder.add_edge(START, "call_llm")
builder.add_conditional_edges(
    "call_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)

# %%
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# %%
initial_state = State(
    messages=[HumanMessage(
        content="Process admission of Scott Bentton who is 15 years old using the tool")]
)
initial_input = {"messages": initial_state["messages"], "state": initial_state}

# %%
# Thread
thread = {"configurable": {"thread_id": "1"}}
response = graph.invoke(initial_input, thread)

# %%
if "__interrupt__" in response:
    question = response['__interrupt__'][0].value
    user_approval = input(question)

    # Check approval
    if user_approval.lower() == "yes":
        graph.invoke(Command(resume=True), thread)
    else:
        print("Sorry! Cannot process the admission!")


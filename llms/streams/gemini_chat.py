from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

gemini = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

messages = [SystemMessage("Give short answers"), 
            HumanMessage ("Who is Guido Van Rossum and what is he upto now?")]

response = gemini.stream(messages)

for chunk in response:
    print(chunk.content, end ='\n\n', flush=True)


 


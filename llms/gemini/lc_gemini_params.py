from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
model = init_chat_model("gemini-2.5-flash",
                        model_provider="google_genai",
                        temperature=0.7,
                        max_output_tokens=200)
response = model.invoke(
      [HumanMessage(content="Write a short story about Moon in 5 sentences")])
print(response.content)

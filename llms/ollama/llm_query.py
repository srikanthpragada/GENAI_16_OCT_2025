from langchain_ollama import OllamaLLM
 
model = OllamaLLM(model="gpt-oss:20b")
print(model.invoke("Which is the capital of Spain? Just give name."))

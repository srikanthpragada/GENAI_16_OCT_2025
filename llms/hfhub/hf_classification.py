from huggingface_hub import InferenceClient
import os

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

model_id = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"   
client = InferenceClient(model=model_id, token = token)

result = client.text_classification("Food in that place is awful")
print(result)

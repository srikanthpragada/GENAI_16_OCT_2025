
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(override=True)  # Loads variables from .env

api_key = os.getenv("OPENAI_API_KEY")
print(api_key)

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4o-mini",
    input="What is the capital of Spain?"
)

print(response.output_text)


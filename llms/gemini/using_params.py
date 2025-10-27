# pip install langchain-google-genai google-generativeai
# Create key using https://aistudio.google.com/apikey

from google import genai
from google.genai.types import GenerateContentConfig

client = genai.Client()

config = GenerateContentConfig(
    temperature=0.8,
    max_output_tokens=200
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="write about sun. Keep it short",
    config = config
)

print(response.text)

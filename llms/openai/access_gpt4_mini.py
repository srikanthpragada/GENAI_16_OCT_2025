# pip install openai
# Create key using https://platform.openai.com/api-keys
# Set environment variable OPENAI_API_KEY to OpenAI key.

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o-mini",
    input="What is the capital of Spain?"
)

print(response.output_text)

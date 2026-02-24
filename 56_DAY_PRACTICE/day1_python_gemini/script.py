from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Create client with API key directly
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain RAG in one sentence"
)

print("🤖 Gemini says:")
print(response.text)

"""
Step 4: Call Vertex AI Gemini from Python using new google.genai client
Run: python3 vertex_ai_demo.py
"""

import google.genai as genai
from google.genai import types

# Initialize with your project
PROJECT_ID = "e2e-etl-project"
LOCATION = "us-central1"

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Generate content using Gemini 2.5
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Explain what Vertex AI is in 2 sentences",
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=256,
    )
)

print("Response from Gemini:")
print(response.text)

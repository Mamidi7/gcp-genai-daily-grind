"""
Cloud Function: Hello Gemini
"""

import google.genai as genai
from google.genai import types
import functions_framework

@functions_framework.http
def hello_gemini(request):
    # Initialize Vertex AI
    client = genai.Client(
        vertexai=True,
        project="e2e-etl-project",
        location="us-central1"
    )

    # Get prompt from request
    request_json = request.get_json(silent=True)
    prompt = request_json.get("prompt", "Hello! Say hi in 2 words.")

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    )

    return response.text, 200

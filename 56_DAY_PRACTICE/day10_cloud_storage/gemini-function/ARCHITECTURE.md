# Gemini Cloud Function - Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER                                             │
│                                                                             │
│  curl -X POST "https://hello-gemini-xxx.us-central1.run.app"              │
│  -d '{"prompt": "What is GCP?"}'                                          │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CLOUD RUN FUNCTIONS                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  hello-gemini (Python 3.11)                                         │   │
│  │                                                                     │   │
│  │  @functions_framework.http                                          │   │
│  │  def hello_gemini(request):                                         │   │
│  │      client = genai.Client(...)  ◄── Step 1: Initialize Vertex AI  │   │
│  │      response = client.models.generate_content(...)  ◄── Step 2    │   │
│  │      return response.text  ◄── Step 3: Return response             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                                   │ HTTPS (JSON)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VERTEX AI                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Model: gemini-2.0-flash-001                                        │   │
│  │  Region: us-central1                                                │   │
│  │  Project: e2e-etl-project                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────┬────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE                                            │
│                                                                             │
│  "GCP (Google Cloud Platform) is a suite of cloud computing..."           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Flow

```
1. USER                    2. CLOUD FUNCTION              3. VERTEX AI
   sends JSON ──────────► receives request ──────────► calls Gemini
   {prompt: "?"}            parses JSON                   generates response
                            calls Vertex AI
                            returns text
```

---

## Code Flow

```python
# main.py structure

@functions_framework.http          # ┐
def hello_gemini(request):         # ├─ Entry point (hello_gemini)
    """Handle HTTP request"""      # │

    # Step 1: Initialize client
    client = genai.Client(
        vertexai=True,             # Use Vertex AI (not Gemini API directly)
        project="e2e-etl-project",
        location="us-central1"
    )

    # Step 2: Get prompt from request
    request_json = request.get_json()
    prompt = request_json.get("prompt", "Hello!")

    # Step 3: Call Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    )

    # Step 4: Return response
    return response.text, 200
```

---

## Files in Package

```
gemini-function/
├── main.py               # Your function code (above)
├── requirements.txt     # Dependencies
│
├── functions-framework==3.*   # Flask-like wrapper for Cloud Run
└── google-genai==1.64.0      # Gemini client
```

---

## How Deployment Works

```
LOCAL MACHINE                          CLOUD CONSOLE

main.py ──────────────────────────► Upload to Console
requirements.txt ──────────────────►

                              ┌────────▼────────┐
                              │  Cloud Run      │
                              │  Functions      │
                              │  (Serverless)   │
                              └────────┬────────┘
                                       │
                              https://hello-gemini-xxx.run.app
                                       │
                              ┌────────▼────────┐
                              │  Ready to       │
                              │  accept HTTP    │
                              │  requests!      │
                              └─────────────────┘
```

---

## Key Interview Points

| Concept | What it does |
|---------|--------------|
| **functions-framework** | Wraps your Python function to handle HTTP requests |
| **@functions_framework.http** | Decorator that makes function respond to HTTP |
| **genai.Client(vertexai=True)** | Connects to Vertex AI (not Gemini REST API) |
| **e2e-etl-project** | Your GCP project where resources live |
| **us-central1** | Region where your function runs |

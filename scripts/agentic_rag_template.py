import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
)
import rag_hybrid  # Reusing our existing hybrid retrieval logic
import json
import random

# Initialize Vertex AI
vertexai.init(project="e2e-etl-project", location="us-central1")

# --- 1. Define Tools (Function Declarations) ---

# Tool A: Knowledge Base Search
search_tool_func = FunctionDeclaration(
    name="search_knowledge_base",
    description="Search the internal knowledge base for information about Kadapa Smart City, traffic, or other local data.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The specific topic or question to search for in the knowledge base."
            }
        },
        "required": ["query"]
    },
)

# Tool B: Get Current Weather (Mock)
weather_tool_func = FunctionDeclaration(
    name="get_current_weather",
    description="Get the current weather conditions for a specific location.",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g., 'San Francisco, CA' or 'Kadapa, AP'."
            }
        },
        "required": ["location"]
    },
)

# Tool C: SQL Calculator (Mock for structured data queries)
sql_tool_func = FunctionDeclaration(
    name="run_sql_query",
    description="Run a SQL query against the 'traffic_analytics' database to get structured statistics.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The SQL query to execute."
            }
        },
        "required": ["query"]
    },
)

# Create the Tool object combining all functions
agent_tools = Tool(
    function_declarations=[search_tool_func, weather_tool_func, sql_tool_func],
)

# --- 2. Load the Model with Tools ---
model = GenerativeModel(
    "gemini-2.5-flash", # Use the latest flash model for speed and tool calling
    tools=[agent_tools],
)

# --- 3. Build the Knowledge Base (Hybrid Index) once ---
print("🚀 Initializing Agentic RAG System...")
vector_store, keyword_store = rag_hybrid.build_stores()

# --- 4. Helper Function to Execute Tool Calls ---
def execute_tool_call(function_call):
    """Executes the tool logic based on Gemini's request."""
    fname = function_call.name
    args = function_call.args
    
    if fname == "search_knowledge_base":
        query = args["query"]
        print(f"🕵️  [Tool: Knowledge Base] Searching for: '{query}'...")
        results = rag_hybrid.hybrid_retrieve(query, vector_store, keyword_store)
        return "\n".join(results) if results else "No relevant information found."
    
    elif fname == "get_current_weather":
        location = args["location"]
        print(f"🌤️  [Tool: Weather] Checking weather for: '{location}'...")
        # Mock weather data
        conditions = ["Sunny", "Cloudy", "Rainy", "Humid"]
        temp = random.randint(25, 40)
        return json.dumps({"location": location, "temperature": f"{temp}°C", "condition": random.choice(conditions)})
    
    elif fname == "run_sql_query":
        query = args["query"]
        print(f"📊 [Tool: SQL] Executing: '{query}'...")
        # Mock SQL execution
        if "COUNT" in query.upper():
            return json.dumps({"result": 42})
        return json.dumps({"result": "Query executed successfully. Traffic data updated."})
    
    return "Error: Unknown tool."

# --- 5. The Agent Loop (Chat) ---
def run_agent():
    chat = model.start_chat()
    
    print("\n🤖 Agentic RAG is Online! (I can search docs, check weather, and run SQL)")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting...")
            break
            
        # Send message to model
        response = chat.send_message(user_input)
        
        # Check for function calls
        # Gemini 2.0 Flash can return multiple function calls in one turn!
        # We need to handle them sequentially.
        try:
            candidate = response.candidates[0]
            parts = candidate.content.parts
        except IndexError:
            print("Agent: (No response generated)")
            continue
            
        # Flag to track if we handled any tool calls
        tool_calls_handled = False
        
        # Iterate through all parts to find function calls
        for part in parts:
            if part.function_call:
                tool_calls_handled = True
                function_call = part.function_call
                
                # Execute the tool
                tool_result = execute_tool_call(function_call)
                
                # Send the tool output back to the model
                # Note: For multiple tools, we might need to send them all back.
                # Simplification: We send the response immediately for each tool.
                # In a robust system, we'd collect all results and send them in one go if the API supports it,
                # or handle the chat history carefully.
                response = chat.send_message(
                    Part.from_function_response(
                        name=function_call.name,
                        response={"content": tool_result},
                    )
                )

        # If we handled tools, the 'response' variable now holds the Final Answer from the model
        # If we didn't handle tools, 'response' holds the initial text response.
        
        # Safely print the text response
        # We use a helper to extract text and ignore function call parts to prevent crashes
        final_text = ""
        for part in response.candidates[0].content.parts:
            if part.text:
                final_text += part.text
        
        if final_text:
            print(f"Agent: {final_text}\n")
        elif not tool_calls_handled:
             # Fallback if no text and no tools (rare)
            print(f"Agent: [Non-text response received]\n")

if __name__ == "__main__":
    run_agent()

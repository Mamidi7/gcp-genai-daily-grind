# Day 7 Exercises: REST APIs with requests

import requests


# Exercise 1: GET Request
# Fetch data from a public API and print the title
def fetch_post():
    """Fetch post #5 from JSONPlaceholder and print its title"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/5")
    data = response.json()
    return data['title']


# Exercise 2: POST Request
# Send data to create a new resource
def create_post(title, body, user_id):
    """
    Create a new post and return the created post's ID.
    POST to: https://jsonplaceholder.typicode.com/posts
    Send JSON: {"title": title, "body": body, "userId": user_id}
    Return the 'id' field from the response
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    post_data = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    response = requests.post(url, json=post_data)
    created = response.json()
    return created['id']


# Exercise 3: Error Handling
# Handle API errors gracefully
def fetch_with_error_handling(url):
    """
    Fetch from URL with proper error handling.
    Return {"success": True, "data": ...} or {"success": False, "error": ...}
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}


# Exercise 4: Call Gemini API
# Call Gemini 2.0 Flash without the SDK
def call_gemini(prompt, api_key):
    """
    Call Gemini API directly using requests.

    URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=KEY
    Headers: {"Content-Type": "application/json"}
    Body: {"contents": [{"parts": [{"text": prompt}]}]}

    Return the generated text
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} — {response.text}")

    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']


# Exercise 5: Query Parameters
# Use query parameters in GET request
def search_posts(query):
    """
    Search posts containing the query word.
    Uses full-text search: https://jsonplaceholder.typicode.com/posts?q={query}
    """
    params = {"q": query}
    response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
    return response.json()


# Run all completed exercises
if __name__ == "__main__":
    import os

    print("=== Exercise 1: GET Request ===")
    print(fetch_post())

    print("\n=== Exercise 2: POST Request ===")
    post_id = create_post("My Title", "My body content", 1)
    print(f"Created post with ID: {post_id}")

    print("\n=== Exercise 3: Error Handling ===")
    result = fetch_with_error_handling("https://jsonplaceholder.typicode.com/posts/1")
    print(result)

    print("\n=== Exercise 4: Gemini API ===")
    try:
        key = os.environ.get("GEMINI_API_KEY", "")
        if key:
            gemini_result = call_gemini("Explain RAG in one sentence.", key)
            print(f"Gemini says: {gemini_result[:100]}...")
        else:
            print("Skipped — no GEMINI_API_KEY set. Run: export GEMINI_API_KEY=your_key")
    except Exception as e:
        print(f"Gemini call failed: {e}")

    print("\n=== Exercise 5: Query Parameters ===")
    results = search_posts("qui")
    print(f"Found {len(results)} posts matching 'qui'")
    if results:
        print(f"First result title: {results[0]['title']}")

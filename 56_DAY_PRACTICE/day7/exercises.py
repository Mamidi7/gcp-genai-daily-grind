# Day 7 Exercises: REST APIs with requests

# Exercise 1: GET Request
# Fetch data from a public API and print the title
def fetch_post():
    """Fetch post #5 from JSONPlaceholder and print its title"""
    # TODO: Use requests.get() to fetch from:
    # https://jsonplaceholder.typicode.com/posts/5
    # Return the title from the response
    pass


# Exercise 2: POST Request
# Create a new post using POST request
def create_post(title, body, user_id):
    """Create a new post and return the created post's ID"""
    # TODO: Use requests.post() to create a post at:
    # https://jsonplaceholder.typicode.com/posts
    # Pass: {"title": title, "body": body, "userId": user_id}
    # Return the ID from the response
    pass


# Exercise 3: Error Handling
# Handle API errors gracefully
def fetch_with_error_handling(url):
    """
    Fetch from URL with proper error handling.
    Return {"success": True, "data": ...} or {"success": False, "error": ...}
    """
    # TODO: Use try/except to handle:
    # - requests.exceptions.ConnectionError
    # - requests.exceptions.Timeout
    # - response.raise_for_status() for 4xx/5xx errors
    pass


# Exercise 4: Call Gemini API
# Call Gemini 2.0 Flash without the SDK
def call_gemini(prompt, api_key):
    """
    Call Gemini API directly using requests.

    URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}
    Headers: {"Content-Type": "application/json"}
    Body: {"contents": [{"parts": [{"text": prompt}]}]}

    Return the generated text
    """
    # TODO: Build the request and extract the answer from response
    # Response format: result['candidates'][0]['content']['parts'][0]['text']
    pass


# Exercise 5: Query Parameters
# Use query parameters in GET request
def search_posts(query):
    """
    Search posts containing the query word.
    Use: https://jsonplaceholder.typicode.com/posts?title={query}
    """
    # TODO: Use params= in requests.get() for query parameters
    pass

# Day 7 Solutions: REST APIs with requests
import requests


# Exercise 1: GET Request
def fetch_post():
    """Fetch post #5 from JSONPlaceholder and print its title"""
    response = requests.get("https://jsonplaceholder.typicode.com/posts/5")
    data = response.json()
    print(f"Title: {data['title']}")
    return data['title']


# Exercise 2: POST Request
def create_post(title, body, user_id):
    """Create a new post and return the created post's ID"""
    post_data = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=post_data)
    data = response.json()
    print(f"Created post with ID: {data['id']}")
    return data['id']


# Exercise 3: Error Handling
def fetch_with_error_handling(url):
    """Fetch from URL with proper error handling"""
    try:
        response = requests.get(url, timeout)
        response.=10raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e}"}


# Exercise 4: Call Gemini API
def call_gemini(prompt, api_key):
    """Call Gemini API directly using requests"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


# Exercise 5: Query Parameters
def search_posts(query):
    """Search posts containing the query word"""
    params = {"title": query}
    response = requests.get("https://jsonplaceholder.typicode.com/posts", params=params)
    return response.json()


# Test all functions
if __name__ == "__main__":
    print("=== Testing Exercises ===\n")

    print("Exercise 1: GET Request")
    fetch_post()

    print("\nExercise 2: POST Request")
    create_post("My Title", "My body content", 1)

    print("\nExercise 3: Error Handling")
    result = fetch_with_error_handling("https://jsonplaceholder.typicode.com/posts/1")
    print(result)

    print("\nExercise 4: Gemini API")
    print("Requires GEMINI_API_KEY to be set")

    print("\nExercise 5: Query Parameters")
    results = search_posts("qui")
    print(f"Found {len(results)} posts")

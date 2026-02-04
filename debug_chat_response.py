import requests
import json

def debug_chat_response():
    """Debug the exact format of the chat response"""

    # Register and login to get a valid token
    BASE_URL = "http://127.0.0.1:8000"

    # Register a test user
    auth_data = {
        "email": "debug_test@example.com",
        "password": "debug_password123"
    }

    # Register
    register_resp = requests.post(f"{BASE_URL}/api/auth/register", json=auth_data)
    print(f"Registration: {register_resp.status_code}")

    # Login
    login_resp = requests.post(f"{BASE_URL}/api/auth/login", json=auth_data)
    print(f"Login: {login_resp.status_code}")

    if login_resp.status_code == 200:
        token_data = login_resp.json()
        access_token = token_data.get("access_token")
        user_id = token_data.get("user_id", 7)  # Use the user ID from previous test

        print(f"Using user_id: {user_id}")

        # Test chat with proper auth
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        chat_payload = {
            "message": "Create a test task to verify response format"
        }

        chat_resp = requests.post(
            f"{BASE_URL}/api/{user_id}/chat",
            json=chat_payload,
            headers=headers
        )

        print(f"Chat response status: {chat_resp.status_code}")
        print(f"Chat response headers: {dict(chat_resp.headers)}")

        try:
            response_json = chat_resp.json()
            print(f"Chat response JSON: {json.dumps(response_json, indent=2)}")

            # Check what fields are available
            available_fields = list(response_json.keys())
            print(f"Available fields in response: {available_fields}")

            # Check for the actual response field used by the frontend
            possible_response_fields = ['response', 'response_text', 'message', 'content']
            found_response_field = None
            for field in possible_response_fields:
                if field in response_json:
                    found_response_field = field
                    print(f"Found response field '{field}': {response_json[field]}")
                    break

            if not found_response_field:
                print("No expected response field found!")

        except Exception as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response text: {chat_resp.text}")

if __name__ == "__main__":
    debug_chat_response()
import requests
import json

# Test the backend API endpoints
BASE_URL = "http://127.0.0.1:8000"  # This matches the frontend .env.local

def test_api_health():
    """Test if the API is reachable"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_openapi():
    """Test if OpenAPI docs are available"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"OpenAPI: {response.status_code} - {len(response.json()) if response.status_code == 200 else 'Error'} chars")
        return response.status_code == 200
    except Exception as e:
        print(f"OpenAPI check failed: {e}")
        return False

def test_chat_endpoint_exists():
    """Test if the chat endpoint exists (will fail without proper auth but should return 401/403, not 404)"""
    try:
        response = requests.post(f"{BASE_URL}/api/1/chat",
                              json={"message": "test"},
                              headers={"Authorization": "Bearer dummy_token"})
        print(f"Chat endpoint: {response.status_code} (expected 401/403 for auth failure, not 404)")
        # We expect 401 (Unauthorized) or 403 (Forbidden) if endpoint exists, not 404 (Not Found)
        return response.status_code in [401, 403, 400]  # 400 is also acceptable for bad request
    except Exception as e:
        print(f"Chat endpoint check failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend API connectivity...\n")

    print("1. Testing health endpoint...")
    health_ok = test_api_health()

    print("\n2. Testing OpenAPI endpoint...")
    openapi_ok = test_openapi()

    print("\n3. Testing chat endpoint availability...")
    chat_ok = test_chat_endpoint_exists()

    print(f"\nResults:")
    print(f"- Health endpoint: {'PASS' if health_ok else 'FAIL'}")
    print(f"- OpenAPI endpoint: {'PASS' if openapi_ok else 'FAIL'}")
    print(f"- Chat endpoint available: {'PASS' if chat_ok else 'FAIL'}")

    if health_ok and openapi_ok and chat_ok:
        print("\n[SUCCESS] All API endpoints are accessible! The backend is running properly.")
    else:
        print("\n[FAILURE] Some API endpoints are not accessible. The backend might not be running.")
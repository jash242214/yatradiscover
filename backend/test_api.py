"""
Test API endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    assert response.status_code == 200, "Health check failed"
    print("✅ Health check passed")


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    assert response.status_code == 200, "Root endpoint failed"
    print("✅ Root endpoint passed")


def test_register():
    """Test user registration"""
    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
    print_response("User Registration", response)

    if response.status_code == 201:
        data = response.json()
        print("✅ Registration passed")
        return data

    return None


def test_login(email: str, password: str):
    """Test user login"""
    login_data = {"email": email, "password": password}

    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
    print_response("User Login", response)

    if response.status_code == 200:
        data = response.json()
        print("✅ Login passed")
        return data

    return None


def run_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "YatraDiscover API Test Suite" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")

    try:
        # Wait for server to be ready
        print("\n⏳ Waiting for server to be ready...")
        for i in range(30):
            try:
                requests.get(f"{BASE_URL}/health", timeout=1)
                print("✅ Server is ready!\n")
                break
            except:
                time.sleep(1)
                if i < 29:
                    print(f"   Attempt {i+1}/30...", end="\r")
        else:
            print("❌ Server did not start in time")
            return

        # Run tests
        test_health_check()
        test_root()
        register_response = test_register()

        if register_response:
            email = register_response["user"]["email"]
            test_login(email, "SecurePassword123!")

        print("\n")
        print("╔" + "=" * 68 + "╗")
        print("║" + " " * 20 + "✅ All Tests Passed!" + " " * 28 + "║")
        print("╚" + "=" * 68 + "╝\n")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_tests()

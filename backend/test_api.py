"""
API Test Script
Test the FastAPI endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 80)
    print("🏥 Testing Health Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_root():
    """Test root endpoint"""
    print("\n" + "=" * 80)
    print("🏠 Testing Root Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))


def test_images():
    """Test images endpoint"""
    print("\n" + "=" * 80)
    print("🖼️  Testing Images Endpoint")
    print("=" * 80)
    
    response = requests.get(f"{BASE_URL}/images/sound")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total images: {data['count']}")
    print(f"First image: {data['images'][0]['title']}")


def test_chat():
    """Test chat endpoint"""
    print("\n" + "=" * 80)
    print("💬 Testing Chat Endpoint")
    print("=" * 80)
    
    test_questions = [
        "How does a bell produce sound?",
        "What are vocal cords?",
        "Explain compression and rarefaction"
    ]
    
    for question in test_questions:
        print(f"\n📝 Question: {question}")
        
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"question": question}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Answer: {data['answer'][:200]}...")
            if data.get('image'):
                print(f"🖼️  Image: {data['image']['filename']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)


def main():
    """Run all tests"""
    print("=" * 80)
    print("🧪 API TESTING SUITE")
    print("=" * 80)
    print("\n⚠️  Make sure the server is running: python main.py")
    print("   Or in another terminal: uvicorn main:app --reload\n")
    
    try:
        # Basic endpoints
        test_root()
        test_health()
        test_images()
        
        # Chat endpoint (requires API key)
        test_chat()
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETE!")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("   Please start the server first: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()


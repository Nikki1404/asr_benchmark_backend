#!/usr/bin/env python3
"""
Test script for ASR Benchmark Hub Backend API
Run this after starting the server to verify all endpoints work
"""

import requests
import json
import time

BASE_URL = "http://0.0.0.0:3019"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_get_posts():
    """Test getting all posts"""
    try:
        response = requests.get(f"{BASE_URL}/api/posts")
        assert response.status_code == 200
        posts = response.json()
        print(f"✅ Retrieved {len(posts)} posts")
        return True
    except Exception as e:
        print(f"❌ Get posts failed: {e}")
        return False

def test_create_post():
    """Test creating a new post"""
    try:
        post_data = {
            "title": "Test Post from API",
            "author": "Test Author", 
            "excerpt": "This is a test post created via API",
            "content": "<h2>Test Content</h2><p>This is test content.</p>",
            "benchmark_data": [
                {"model": "Test Model", "wer": 15.5, "dataset": "Test Dataset"}
            ],
            "model_performance_data": [
                {"model": "Test Model", "avgWer": 15.5}
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/posts",
            headers={"Content-Type": "application/json"},
            json=post_data
        )
        assert response.status_code == 200
        new_post = response.json()
        print(f"✅ Created post with ID: {new_post['id']}")
        return True
    except Exception as e:
        print(f"❌ Create post failed: {e}")
        return False

def test_ai_summarize():
    """Test AI summarization"""
    try:
        # This will only work if you have a valid API key
        response = requests.post(
            f"{BASE_URL}/api/ai/summarize",
            headers={"Content-Type": "application/json"},
            json={"content": "This is a test content for summarization. It contains multiple sentences to test the AI summarization feature."}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI summarization worked: {result['summary'][:50]}...")
            return True
        else:
            print(f"⚠️ AI summarization failed (likely no API key): {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ AI summarization error (expected if no API key): {e}")
        return False

def main():
    print("🚀 Testing ASR Benchmark Hub Backend API...")
    print(f"Testing against: {BASE_URL}")
    print("-" * 50)
    
    tests = [
        test_health,
        test_get_posts,
        test_create_post,
        test_ai_summarize,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("-" * 50)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Backend is working correctly.")
    elif passed >= len(tests) - 1:  # Allow AI test to fail
        print("✅ Core functionality working! (AI features may need API key)")
    else:
        print("❌ Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()

"""
Utils Tests
Unit tests for utility functions
"""

import sys
sys.path.append('..')

from utils import sanitize_filename, format_file_size, create_response


def test_sanitize_filename():
    """Test filename sanitization"""
    # Valid filename
    assert sanitize_filename("document.pdf") == "document.pdf"
    
    # Filename with dangerous characters
    result = sanitize_filename("doc<>ument.pdf")
    assert "<" not in result and ">" not in result
    
    # Very long filename
    long_name = "a" * 300 + ".pdf"
    result = sanitize_filename(long_name)
    assert len(result) <= 255
    
    print("✅ Filename sanitization test passed")


def test_format_file_size():
    """Test file size formatting"""
    # Test various sizes
    assert format_file_size(512) == "512.0 B"
    assert format_file_size(1024) == "1.0 KB"
    assert format_file_size(1024 * 1024) == "1.0 MB"
    
    print("✅ File size formatting test passed")


def test_create_response():
    """Test response creation"""
    # Success response
    response = create_response(True, data={"status": "ok"}, message="Success")
    assert response["success"] == True
    assert response["data"]["status"] == "ok"
    assert "timestamp" in response
    
    # Error response
    error_response = create_response(False, error="Something went wrong")
    assert error_response["success"] == False
    assert error_response["error"] == "Something went wrong"
    
    print("✅ Response creation test passed")


if __name__ == "__main__":
    test_sanitize_filename()
    test_format_file_size()
    test_create_response()
    print("\n🎉 Utils tests completed!")

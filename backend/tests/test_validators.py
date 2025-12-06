"""
Unit Tests for Validators
"""

import sys
sys.path.append('..')

from validators import validate_pdf_filename, validate_question, validate_topic_id


def test_validate_pdf_filename():
    """Test PDF filename validation"""
    # Valid cases
    assert validate_pdf_filename("document.pdf")[0] == True
    assert validate_pdf_filename("test_file.pdf")[0] == True
    
    # Invalid cases
    assert validate_pdf_filename("document.txt")[0] == False
    assert validate_pdf_filename("")[0] == False
    assert validate_pdf_filename("file<>.pdf")[0] == False
    
    print("✅ PDF filename validation tests passed")


def test_validate_question():
    """Test question validation"""
    # Valid cases
    assert validate_question("How does sound work?")[0] == True
    assert validate_question("Explain compression")[0] == True
    
    # Invalid cases
    assert validate_question("")[0] == False
    assert validate_question("Hi")[0] == False
    assert validate_question("x" * 1001)[0] == False
    
    print("✅ Question validation tests passed")


def test_validate_topic_id():
    """Test topic ID validation"""
    # Valid cases
    assert validate_topic_id("sound")[0] == True
    assert validate_topic_id("physics_chapter_1")[0] == True
    
    # Invalid cases
    assert validate_topic_id("")[0] == False
    assert validate_topic_id("invalid-id")[0] == False
    assert validate_topic_id("Invalid ID")[0] == False
    
    print("✅ Topic ID validation tests passed")


if __name__ == "__main__":
    test_validate_pdf_filename()
    test_validate_question()
    test_validate_topic_id()
    print("\n🎉 All tests passed!")


"""
PDF Processor Tests
Unit tests for PDF processing functionality
"""

import sys
import os
sys.path.append('..')

from pdf_processor import extract_text_from_pdf, extract_images_from_pdf


def test_extract_text_from_pdf():
    """Test text extraction from PDF"""
    # Test with sample PDF path
    test_pdf = "test_sample.pdf"
    
    if os.path.exists(test_pdf):
        text = extract_text_from_pdf(test_pdf)
        assert text is not None
        assert len(text) > 0
        print("✅ PDF text extraction test passed")
    else:
        print("⚠️ Test PDF not found, skipping text extraction test")


def test_extract_images_from_pdf():
    """Test image extraction from PDF"""
    test_pdf = "test_sample.pdf"
    
    if os.path.exists(test_pdf):
        images = extract_images_from_pdf(test_pdf)
        assert isinstance(images, list)
        print("✅ PDF image extraction test passed")
    else:
        print("⚠️ Test PDF not found, skipping image extraction test")


if __name__ == "__main__":
    test_extract_text_from_pdf()
    test_extract_images_from_pdf()
    print("\n🎉 PDF processor tests completed!")

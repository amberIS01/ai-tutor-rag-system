"""
PDF Processing Module
Handles PDF text extraction and chunking using PyMuPDF
"""

import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os
from typing import List, Dict


class PDFProcessor:
    """Extract and process text from PDF files"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file using PyMuPDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a single string
        """
        print(f"📄 Opening PDF: {pdf_path}")
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        full_text = ""
        
        # Extract text from each page
        total_pages = len(doc)
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            full_text += f"\n--- Page {page_num + 1} ---\n"
            full_text += text
        
        print(f"✅ Extracted {len(full_text)} characters from {total_pages} pages")
        
        doc.close()
        
        return full_text
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        """
        Split text into chunks for RAG retrieval
        
        Args:
            text: Full text to chunk
            
        Returns:
            List of chunk dictionaries with id, text, and metadata
        """
        print(f"✂️  Chunking text...")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create structured chunk objects
        chunk_objects = []
        for idx, chunk_text in enumerate(chunks):
            chunk_obj = {
                "id": f"chunk_{idx:04d}",
                "text": chunk_text,
                "chunk_index": idx,
                "char_count": len(chunk_text)
            }
            chunk_objects.append(chunk_obj)
        
        print(f"✅ Created {len(chunk_objects)} chunks")
        
        return chunk_objects
    
    def process_pdf(self, pdf_path: str, output_path: str = None) -> List[Dict[str, any]]:
        """
        Complete pipeline: Extract text and create chunks
        
        Args:
            pdf_path: Path to PDF file
            output_path: Optional path to save chunks as JSON
            
        Returns:
            List of text chunks
        """
        # Extract text
        full_text = self.extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = self.chunk_text(full_text)
        
        # Save to JSON if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved chunks to: {output_path}")
        
        return chunks


def main():
    """Test the PDF processor"""
    # Initialize processor
    processor = PDFProcessor(chunk_size=1000, chunk_overlap=200)
    
    # Process the Sound.pdf file
    pdf_path = "../Sound.pdf"
    output_path = "data/chunks.json"
    
    print("=" * 60)
    print("🚀 PDF EXTRACTION TEST")
    print("=" * 60)
    
    chunks = processor.process_pdf(pdf_path, output_path)
    
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    print(f"Total chunks: {len(chunks)}")
    print(f"\n📝 Sample chunk (first one):")
    print("-" * 60)
    print(chunks[0]['text'][:500] + "...")
    print("-" * 60)
    print(f"\nChunk ID: {chunks[0]['id']}")
    print(f"Character count: {chunks[0]['char_count']}")


if __name__ == "__main__":
    main()


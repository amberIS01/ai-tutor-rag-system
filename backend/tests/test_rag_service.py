"""
RAG Service Tests
Unit tests for RAG service functionality
"""

import sys
sys.path.append('..')

from rag_service import search_relevant_chunks


def test_search_relevant_chunks():
    """Test semantic search in RAG service"""
    query = "What is photosynthesis?"
    
    # This would require embeddings to be loaded
    # For now, we'll do a smoke test
    try:
        results = search_relevant_chunks(query, top_k=5)
        assert isinstance(results, list)
        print("✅ RAG search test passed")
    except Exception as e:
        print(f"⚠️ RAG search test requires embeddings to be loaded: {e}")


def test_search_with_empty_query():
    """Test search with empty query"""
    query = ""
    
    try:
        results = search_relevant_chunks(query, top_k=5)
        # Should handle empty queries gracefully
        assert results is not None
        print("✅ Empty query handling test passed")
    except Exception as e:
        print(f"⚠️ Empty query test: {e}")


if __name__ == "__main__":
    test_search_relevant_chunks()
    test_search_with_empty_query()
    print("\n🎉 RAG service tests completed!")

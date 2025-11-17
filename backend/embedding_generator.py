"""
Embedding Generation Module
Generates vector embeddings for text chunks and image metadata
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os


class EmbeddingGenerator:
    """Generate embeddings using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        print(f"🤖 Loading embedding model: {model_name}")
        print("📥 (First time will download ~80MB, subsequent runs are instant)")
        
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        print(f"✅ Model loaded! Embedding dimension: {self.embedding_dim}")
    
    def generate_text_embeddings(self, chunks_file: str) -> tuple:
        """
        Generate embeddings for all text chunks
        
        Args:
            chunks_file: Path to chunks.json file
            
        Returns:
            Tuple of (embeddings_array, chunk_ids, chunks_data)
        """
        print(f"\n📄 Loading chunks from: {chunks_file}")
        
        # Load chunks
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f"✅ Loaded {len(chunks)} chunks")
        
        # Extract texts and IDs
        texts = [chunk['text'] for chunk in chunks]
        chunk_ids = [chunk['id'] for chunk in chunks]
        
        print(f"🔄 Generating embeddings for {len(texts)} chunks...")
        print("   (This may take 10-30 seconds)")
        
        # Generate embeddings in batch (much faster!)
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True
        )
        
        print(f"✅ Generated {len(embeddings)} embeddings")
        print(f"   Shape: {embeddings.shape}")
        
        return embeddings, chunk_ids, chunks
    
    def generate_image_embeddings(self, metadata_file: str) -> tuple:
        """
        Generate embeddings for image metadata
        
        Args:
            metadata_file: Path to image_metadata.json file
            
        Returns:
            Tuple of (embeddings_array, image_ids, image_data)
        """
        print(f"\n🖼️  Loading image metadata from: {metadata_file}")
        
        # Load metadata
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        images = data['images']
        print(f"✅ Loaded {len(images)} images")
        
        # Create rich text representations for each image
        # Combine title, description, and keywords for better matching
        texts = []
        image_ids = []
        
        for img in images:
            # Create a comprehensive text representation
            keywords_str = ", ".join(img['keywords'])
            topics_str = ", ".join(img['topics'])
            
            rich_text = (
                f"{img['title']}. "
                f"{img['description']} "
                f"Keywords: {keywords_str}. "
                f"Topics: {topics_str}."
            )
            
            texts.append(rich_text)
            image_ids.append(img['id'])
        
        print(f"🔄 Generating embeddings for {len(texts)} images...")
        
        # Generate embeddings
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32,
            convert_to_numpy=True
        )
        
        print(f"✅ Generated {len(embeddings)} image embeddings")
        print(f"   Shape: {embeddings.shape}")
        
        return embeddings, image_ids, images
    
    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate embedding for a single query
        
        Args:
            query: User's question or search query
            
        Returns:
            Embedding vector as numpy array
        """
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding


def main():
    """Test the embedding generator"""
    print("=" * 70)
    print("🚀 EMBEDDING GENERATION TEST")
    print("=" * 70)
    
    # Initialize generator
    generator = EmbeddingGenerator()
    
    # Generate text embeddings
    text_embeddings, chunk_ids, chunks = generator.generate_text_embeddings(
        "data/chunks.json"
    )
    
    # Generate image embeddings
    image_embeddings, image_ids, images = generator.generate_image_embeddings(
        "data/image_metadata.json"
    )
    
    # Test query embedding
    print("\n" + "=" * 70)
    print("🔍 TESTING QUERY EMBEDDING")
    print("=" * 70)
    
    test_query = "How does a bell produce sound?"
    print(f"Query: '{test_query}'")
    
    query_embedding = generator.generate_query_embedding(test_query)
    print(f"✅ Query embedding shape: {query_embedding.shape}")
    print(f"   First 5 values: {query_embedding[:5]}")
    
    # Calculate similarity with first chunk (manual test)
    from numpy.linalg import norm
    
    def cosine_similarity(a, b):
        return np.dot(a, b) / (norm(a) * norm(b))
    
    similarity = cosine_similarity(query_embedding, text_embeddings[0])
    print(f"\n📊 Similarity with first chunk: {similarity:.4f}")
    print(f"   Chunk text preview: {chunks[0]['text'][:100]}...")
    
    print("\n" + "=" * 70)
    print("✅ EMBEDDING GENERATION COMPLETE!")
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"   - Text embeddings: {text_embeddings.shape}")
    print(f"   - Image embeddings: {image_embeddings.shape}")
    print(f"   - Embedding dimension: {generator.embedding_dim}")
    print(f"   - Ready for FAISS indexing!")


if __name__ == "__main__":
    main()


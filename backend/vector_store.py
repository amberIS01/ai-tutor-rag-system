"""
Vector Store Module
Handles FAISS indexing and similarity search
"""

import faiss
import numpy as np
import json
import os
from typing import List, Dict, Tuple
from embedding_generator import EmbeddingGenerator


class VectorStore:
    """Manage FAISS vector indices for text and images"""
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize vector store
        
        Args:
            embedding_dim: Dimension of embedding vectors
        """
        self.embedding_dim = embedding_dim
        self.text_index = None
        self.image_index = None
        self.chunk_mapping = {}
        self.image_mapping = {}
    
    def create_text_index(self, embeddings: np.ndarray, chunk_ids: List[str], 
                          chunks: List[Dict]) -> None:
        """
        Create FAISS index for text chunks
        
        Args:
            embeddings: Array of embedding vectors
            chunk_ids: List of chunk IDs
            chunks: List of chunk data dictionaries
        """
        print(f"\n🗄️  Creating FAISS index for text...")
        
        # Create FAISS index (L2 distance)
        self.text_index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Add vectors to index
        self.text_index.add(embeddings.astype('float32'))
        
        # Create mapping from index position to chunk data
        self.chunk_mapping = {
            i: {
                'chunk_id': chunk_ids[i],
                'text': chunks[i]['text'],
                'chunk_index': chunks[i]['chunk_index']
            }
            for i in range(len(chunk_ids))
        }
        
        print(f"✅ Text index created!")
        print(f"   Vectors in index: {self.text_index.ntotal}")
        print(f"   Index type: IndexFlatL2 (100% accurate)")
    
    def create_image_index(self, embeddings: np.ndarray, image_ids: List[str],
                          images: List[Dict]) -> None:
        """
        Create FAISS index for image metadata
        
        Args:
            embeddings: Array of embedding vectors
            image_ids: List of image IDs
            images: List of image metadata dictionaries
        """
        print(f"\n🗄️  Creating FAISS index for images...")
        
        # Create FAISS index
        self.image_index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Add vectors to index
        self.image_index.add(embeddings.astype('float32'))
        
        # Create mapping
        self.image_mapping = {
            i: {
                'image_id': image_ids[i],
                'filename': images[i]['filename'],
                'title': images[i]['title'],
                'description': images[i]['description'],
                'keywords': images[i]['keywords']
            }
            for i in range(len(image_ids))
        }
        
        print(f"✅ Image index created!")
        print(f"   Vectors in index: {self.image_index.ntotal}")
    
    def search_text(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Search for similar text chunks
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of matching chunks with scores
        """
        if self.text_index is None:
            raise ValueError("Text index not initialized!")
        
        # Reshape for FAISS (needs 2D array)
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        distances, indices = self.text_index.search(query_vector, k)
        
        # Format results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            chunk_data = self.chunk_mapping[idx]
            results.append({
                'rank': i + 1,
                'chunk_id': chunk_data['chunk_id'],
                'text': chunk_data['text'],
                'distance': float(distance),
                'similarity_score': self._distance_to_similarity(distance)
            })
        
        return results
    
    def search_images(self, query_embedding: np.ndarray, k: int = 1) -> List[Dict]:
        """
        Search for similar images
        
        Args:
            query_embedding: Query vector
            k: Number of results to return (usually 1 for images)
            
        Returns:
            List of matching images with scores
        """
        if self.image_index is None:
            raise ValueError("Image index not initialized!")
        
        # Reshape for FAISS
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        distances, indices = self.image_index.search(query_vector, k)
        
        # Format results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            image_data = self.image_mapping[idx]
            results.append({
                'rank': i + 1,
                'image_id': image_data['image_id'],
                'filename': image_data['filename'],
                'title': image_data['title'],
                'description': image_data['description'],
                'keywords': image_data['keywords'],
                'distance': float(distance),
                'similarity_score': self._distance_to_similarity(distance)
            })
        
        return results
    
    def _distance_to_similarity(self, distance: float) -> float:
        """
        Convert L2 distance to similarity score (0-1)
        Lower distance = Higher similarity
        """
        # Simple conversion: inverse with normalization
        # This gives scores roughly between 0-1
        similarity = 1 / (1 + distance)
        return similarity
    
    def save_indices(self, save_dir: str) -> None:
        """
        Save FAISS indices and mappings to disk
        
        Args:
            save_dir: Directory to save files
        """
        print(f"\n💾 Saving indices to: {save_dir}")
        
        os.makedirs(save_dir, exist_ok=True)
        
        # Save FAISS indices
        if self.text_index is not None:
            faiss.write_index(self.text_index, os.path.join(save_dir, "text_vectors.index"))
            print(f"✅ Saved text_vectors.index")
        
        if self.image_index is not None:
            faiss.write_index(self.image_index, os.path.join(save_dir, "image_vectors.index"))
            print(f"✅ Saved image_vectors.index")
        
        # Save mappings
        with open(os.path.join(save_dir, "chunk_mapping.json"), 'w', encoding='utf-8') as f:
            json.dump(self.chunk_mapping, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved chunk_mapping.json")
        
        with open(os.path.join(save_dir, "image_mapping.json"), 'w', encoding='utf-8') as f:
            json.dump(self.image_mapping, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved image_mapping.json")
        
        print(f"✅ All indices saved successfully!")
    
    def load_indices(self, load_dir: str) -> None:
        """
        Load FAISS indices and mappings from disk
        
        Args:
            load_dir: Directory containing saved files
        """
        print(f"\n📂 Loading indices from: {load_dir}")
        
        # Load FAISS indices
        text_index_path = os.path.join(load_dir, "text_vectors.index")
        if os.path.exists(text_index_path):
            self.text_index = faiss.read_index(text_index_path)
            print(f"✅ Loaded text_vectors.index ({self.text_index.ntotal} vectors)")
        
        image_index_path = os.path.join(load_dir, "image_vectors.index")
        if os.path.exists(image_index_path):
            self.image_index = faiss.read_index(image_index_path)
            print(f"✅ Loaded image_vectors.index ({self.image_index.ntotal} vectors)")
        
        # Load mappings
        with open(os.path.join(load_dir, "chunk_mapping.json"), 'r', encoding='utf-8') as f:
            # Convert string keys back to integers
            self.chunk_mapping = {int(k): v for k, v in json.load(f).items()}
        print(f"✅ Loaded chunk_mapping.json")
        
        with open(os.path.join(load_dir, "image_mapping.json"), 'r', encoding='utf-8') as f:
            self.image_mapping = {int(k): v for k, v in json.load(f).items()}
        print(f"✅ Loaded image_mapping.json")
        
        print(f"✅ All indices loaded successfully!")


def main():
    """Build complete vector store"""
    print("=" * 70)
    print("🚀 BUILDING VECTOR STORE")
    print("=" * 70)
    
    # Step 1: Generate embeddings
    generator = EmbeddingGenerator()
    
    text_embeddings, chunk_ids, chunks = generator.generate_text_embeddings(
        "data/chunks.json"
    )
    
    image_embeddings, image_ids, images = generator.generate_image_embeddings(
        "data/image_metadata.json"
    )
    
    # Step 2: Create FAISS indices
    vector_store = VectorStore(embedding_dim=generator.embedding_dim)
    
    vector_store.create_text_index(text_embeddings, chunk_ids, chunks)
    vector_store.create_image_index(image_embeddings, image_ids, images)
    
    # Step 3: Test search
    print("\n" + "=" * 70)
    print("🔍 TESTING SEARCH")
    print("=" * 70)
    
    test_query = "How does a bell produce sound through vibration?"
    print(f"\n📝 Query: '{test_query}'")
    
    query_embedding = generator.generate_query_embedding(test_query)
    
    # Search text
    print(f"\n🔎 Top 3 matching text chunks:")
    text_results = vector_store.search_text(query_embedding, k=3)
    for result in text_results:
        print(f"\n  Rank {result['rank']}: {result['chunk_id']}")
        print(f"  Similarity: {result['similarity_score']:.4f}")
        print(f"  Text preview: {result['text'][:150]}...")
    
    # Search images
    print(f"\n🖼️  Best matching image:")
    image_results = vector_store.search_images(query_embedding, k=1)
    for result in image_results:
        print(f"\n  Image: {result['filename']}")
        print(f"  Title: {result['title']}")
        print(f"  Similarity: {result['similarity_score']:.4f}")
        print(f"  Description: {result['description'][:100]}...")
    
    # Step 4: Save everything
    vector_store.save_indices("data/embeddings")
    
    print("\n" + "=" * 70)
    print("✅ VECTOR STORE BUILD COMPLETE!")
    print("=" * 70)
    print("📊 Summary:")
    print(f"   - Text vectors: {text_embeddings.shape[0]}")
    print(f"   - Image vectors: {image_embeddings.shape[0]}")
    print(f"   - Dimension: {generator.embedding_dim}")
    print(f"   - Saved to: data/embeddings/")
    print(f"\n🎉 Ready for RAG chatbot!")


if __name__ == "__main__":
    main()


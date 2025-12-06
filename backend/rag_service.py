"""
RAG Service Module
Handles retrieval augmented generation logic
"""

import json
import requests
from typing import List, Dict, Tuple
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from config import config


class RAGService:
    """RAG service for question answering with context"""
    
    def __init__(self):
        """Initialize RAG components"""
        print("🔧 Initializing RAG Service...")
        
        # Load embedding generator
        self.generator = EmbeddingGenerator()
        
        # Load vector store
        self.vector_store = VectorStore(embedding_dim=384)
        self.vector_store.load_indices(config.EMBEDDINGS_DIR)
        
        print("✅ RAG Service ready!")
    
    def retrieve_context(self, question: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Retrieve relevant chunks and images for a question
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (text_chunks, images)
        """
        # Generate query embedding
        query_embedding = self.generator.generate_query_embedding(question)
        
        # Retrieve text chunks
        text_results = self.vector_store.search_text(
            query_embedding, 
            k=config.TOP_K_CHUNKS
        )
        
        # Retrieve relevant image
        image_results = self.vector_store.search_images(
            query_embedding,
            k=config.TOP_K_IMAGES
        )
        
        return text_results, image_results
    
    def generate_answer(self, question: str, context_chunks: List[Dict]) -> str:
        """
        Generate answer using LLM with retrieved context
        
        Args:
            question: User's question
            context_chunks: Retrieved text chunks
            
        Returns:
            Generated answer
        """
        # Build context from chunks
        context_text = "\n\n".join([
            f"Context {i+1}:\n{chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        # Create prompt
        system_prompt = """You are an expert physics tutor teaching students from their textbook. 

CRITICAL RULES:
- ONLY use information from the provided context below
- DO NOT add any information from your general knowledge
- DO NOT make up or assume any facts
- If the answer is NOT in the provided context, clearly state: "I don't have that information in the current chapter."
- Always cite which context section you're using when possible

Your role:
- Explain concepts clearly and simply using ONLY the provided context
- Be encouraging and supportive
- Keep answers concise but complete (2-4 paragraphs)
- If you're unsure, say so rather than guessing"""

        user_prompt = f"""Context from the textbook:

{context_text}

---

Student's Question: {question}

Instructions: Answer this question using ONLY the information provided in the context above. Do not use any external knowledge. If the context doesn't contain the answer, say "I don't have that information in this chapter." """

        # Call OpenRouter API
        try:
            response = requests.post(
                config.OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "AI Tutor RAG System"
                },
                json={
                    "model": config.MODEL_NAME,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=60  # Increased timeout for reliability
            )
            
            response.raise_for_status()
            result = response.json()
            
            answer = result["choices"][0]["message"]["content"]
            return answer
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling OpenRouter API: {e}")
            
            # Fallback: Return context-based answer
            fallback_answer = f"""I'm having trouble connecting to the AI service right now. 

However, based on the relevant section from your textbook:

{context_chunks[0]['text'][:500]}...

This should help answer your question about: {question}"""
            
            return fallback_answer
    
    def answer_question(self, question: str) -> Dict:
        """
        Complete RAG pipeline: retrieve context and generate answer
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer, chunks, and image
        """
        print(f"\n🔍 Processing question: {question}")
        
        # Retrieve context
        text_chunks, images = self.retrieve_context(question)
        
        print(f"✅ Retrieved {len(text_chunks)} chunks and {len(images)} image(s)")
        
        # Generate answer
        answer = self.generate_answer(question, text_chunks)
        
        print(f"✅ Generated answer ({len(answer)} chars)")
        
        # Prepare response
        response = {
            "question": question,
            "answer": answer,
            "context_chunks": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "text": chunk["text"][:200] + "...",  # Truncate for response
                    "similarity": chunk["similarity_score"]
                }
                for chunk in text_chunks
            ],
            "image": images[0] if images else None
        }
        
        return response


# Initialize service (singleton)
rag_service = None

def get_rag_service() -> RAGService:
    """Get or create RAG service instance"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service


"""
Vector Store Module

Manages the vector database for semantic search of clinics
"""

import os
import json
from typing import List, Dict, Optional
try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.schema import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not fully available. Some features may be limited.")


class VectorStore:
    """Manage vector database for clinic data"""
    
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        self.vectorstore = None
        
        if LANGCHAIN_AVAILABLE:
            try:
                self.embeddings = OpenAIEmbeddings()
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI embeddings: {e}")
                self.embeddings = None
        else:
            self.embeddings = None
    
    def create_from_clinics(self, clinics: List[Dict]):
        """
        Create vector store from clinic data
        
        Args:
            clinics: List of clinic dictionaries
        """
        if not LANGCHAIN_AVAILABLE or not self.embeddings:
            print("LangChain or embeddings not available. Skipping vector store creation.")
            return
        
        documents = []
        for clinic in clinics:
            # Create searchable text from clinic data
            content = f"""
            Clinic: {clinic.get('name', '')}
            Category: {clinic.get('category', '')}
            Location: {clinic.get('area', '')}, {clinic.get('location', '')}
            Description: {clinic.get('description', '')}
            Services: {', '.join(clinic.get('services', []))}
            Rating: {clinic.get('rating', 'N/A')}/5 ({clinic.get('review_count', 0)} reviews)
            Price Range: {clinic.get('price_range', 'N/A')}
            Features: {', '.join(clinic.get('features', []))}
            Access: {clinic.get('access', '')}
            """
            
            doc = Document(
                page_content=content,
                metadata={
                    'id': clinic.get('id', ''),
                    'name': clinic.get('name', ''),
                    'category': clinic.get('category', ''),
                    'location': clinic.get('location', ''),
                    'area': clinic.get('area', ''),
                    'rating': clinic.get('rating', 0),
                    'clinic_data': json.dumps(clinic)
                }
            )
            documents.append(doc)
        
        try:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            print(f"Created vector store with {len(documents)} clinics")
        except Exception as e:
            print(f"Error creating vector store: {e}")
    
    def load_existing(self):
        """Load existing vector store from disk"""
        if not LANGCHAIN_AVAILABLE or not self.embeddings:
            print("LangChain or embeddings not available.")
            return False
        
        if os.path.exists(self.persist_directory):
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                print("Loaded existing vector store")
                return True
            except Exception as e:
                print(f"Error loading vector store: {e}")
                return False
        return False
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Search for clinics using semantic search
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of clinic dictionaries
        """
        if not self.vectorstore:
            print("Vector store not initialized")
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            clinics = []
            
            for doc in results:
                clinic_data = json.loads(doc.metadata.get('clinic_data', '{}'))
                clinics.append(clinic_data)
            
            return clinics
        except Exception as e:
            print(f"Search error: {e}")
            return []


if __name__ == "__main__":
    # Test vector store
    from scraper.data_processor import DataProcessor
    
    processor = DataProcessor()
    clinics = processor.load_clinics()
    
    if clinics:
        vs = VectorStore()
        vs.create_from_clinics(clinics)
        
        results = vs.search("facial treatment in Shibuya", k=3)
        print(f"\nSearch results: {len(results)} clinics")
        for clinic in results:
            print(f"  - {clinic['name']} ({clinic['area']})")

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class ChromaDBHandler:
    def __init__(self, persist_directory: str, Unique_db: str):
        print(f"Initializing ChromaDB with persist directory: {persist_directory}")
        self.client = chromadb.Client(Settings(persist_directory=persist_directory))
        print("ChromaDB client initialized successfully")
        
        self.collection = self.client.get_or_create_collection(name=Unique_db)
        print(f"Collection '{Unique_db}' created or retrieved successfully")
        
        # Load Sentence Transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Sentence Transformer model loaded successfully")
    
    def generate_embedding(self, text: str):
        embedding = self.model.encode(text)
        print(f"Generated embedding for text: {text[:50]}...")
        return embedding
    
    def add_document(self, doc_id: str, embedding):
        self.collection.add(embeddings=[embedding.tolist()], ids=[doc_id])
        print(f"Document added with ID: {doc_id}")
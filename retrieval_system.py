import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import document_processor as dp 

class LocalRetrievalSystem:
    """Implements local semantic search using SentenceTransformers and FAISS."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.doc_map = {}

    def build_index(self, input_dir):
        """Extracts text, generates embeddings, and builds the FAISS index."""
        print("Building semantic index...", flush=True)
        
        doc_texts = []
        doc_filenames = []
        
        # Ingest and Extract Text
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.pdf', '.txt')):
                filepath = os.path.join(input_dir, filename)
                text = dp.extract_text_from_pdf(filepath)
                
                if text:
                    doc_texts.append(text)
                    doc_filenames.append(filename)

        if not doc_texts:
            print("No documents found for indexing.", flush=True)
            return

        print(f"Generating embeddings for {len(doc_texts)} documents...", flush=True)
        doc_embeddings = self.model.encode(doc_texts, convert_to_tensor=False)
        
        d = doc_embeddings.shape[1]
        
        # Create FAISS Index
        self.index = faiss.IndexFlatL2(d)
        self.index.add(doc_embeddings.astype('float32'))
        
        self.doc_map = {i: filename for i, filename in enumerate(doc_filenames)}
        
        print("Indexing complete.", flush=True)

    def search(self, query, k=5):
        """Performs semantic search for the query."""
        if self.index is None:
            print("Error: Index is not built. Run build_index() first.", flush=True)
            return []

        query_embedding = self.model.encode([query], convert_to_tensor=False)
        query_embedding = query_embedding.astype('float32')

        D, I = self.index.search(query_embedding, k)
        
        results = []
        for i in range(len(I[0])):
            doc_id = I[0][i]
            if doc_id in self.doc_map:
                results.append((self.doc_map[doc_id], D[0][i]))

        return results
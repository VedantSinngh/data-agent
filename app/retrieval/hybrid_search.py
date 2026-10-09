import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from rank_bm25 import BM25Okapi
from app.retrieval.chunker import DocumentChunk

class HybridRetriever:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: List[DocumentChunk] = []
        self.bm25 = None
        
    def index_documents(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        if not chunks:
            return
            
        # Dense (FAISS) indexing
        texts = [chunk.text for chunk in chunks]
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        # Sparse (BM25) indexing
        tokenized_corpus = [text.lower().split(" ") for text in texts]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        if not self.chunks:
            return []
            
        # 1. Dense Search
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, k)
        
        dense_results = []
        for rank, idx in enumerate(I[0]):
            if idx != -1:
                dense_results.append({
                    "chunk": self.chunks[idx],
                    "dense_score": float(D[0][rank]),
                    "idx": idx
                })
                
        # 2. Sparse Search
        tokenized_query = query.lower().split(" ")
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_n = np.argsort(bm25_scores)[::-1][:k]
        
        sparse_results = []
        for idx in top_n:
            sparse_results.append({
                "chunk": self.chunks[idx],
                "sparse_score": float(bm25_scores[idx]),
                "idx": idx
            })
            
        # 3. Hybrid Fusion (Reciprocal Rank Fusion - simple version)
        fused_scores = {}
        for r, res in enumerate(dense_results):
            idx = res["idx"]
            fused_scores[idx] = fused_scores.get(idx, 0) + 1.0 / (60 + r + 1)
            
        for r, res in enumerate(sparse_results):
            idx = res["idx"]
            fused_scores[idx] = fused_scores.get(idx, 0) + 1.0 / (60 + r + 1)
            
        sorted_indices = sorted(fused_scores.keys(), key=lambda x: fused_scores[x], reverse=True)
        top_k_indices = sorted_indices[:k]
        
        return [
            {
                "chunk_id": self.chunks[idx].chunk_id,
                "text": self.chunks[idx].text,
                "metadata": self.chunks[idx].metadata,
                "fusion_score": fused_scores[idx]
            }
            for idx in top_k_indices
        ]

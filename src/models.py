import os
import pickle
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from preprocessing import preprocess_financial_text

# =====================================================================
# 1. TF-IDF VECTOR SPACE MODEL
# =====================================================================
class TFIDFRetriever:
    def __init__(self, corpus: Dict[str, Dict[str, str]], max_features: int = 50000):
        self.doc_ids = list(corpus.keys())
        self.corpus_texts = [f"{corpus[did]['title']} {corpus[did]['text']}".strip() for did in self.doc_ids]
        
        print(f"⚡ Fitting TF-IDF Vectorizer (max_features={max_features:,})...")
        self.vectorizer = TfidfVectorizer(
            tokenizer=lambda t: preprocess_financial_text(t, apply_stemming=True),
            max_features=max_features,
            sublinear_tf=True,
            norm="l2"
        )
        self.doc_matrix = self.vectorizer.fit_transform(self.corpus_texts)
        print(" TF-IDF model ready.")

    def retrieve(self, query: str, top_k: int = 100) -> List[Tuple[str, float]]:
        q_vec = self.vectorizer.transform([query])
        scores = q_vec.dot(self.doc_matrix.T).toarray().flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self.doc_ids[i], float(scores[i])) for i in top_indices]

    def batch_retrieve(self, queries: Dict[str, str], top_k: int = 100) -> Dict[str, List[str]]:
        results = {}
        qids = list(queries.keys())
        q_texts = [queries[qid] for qid in qids]
        q_matrix = self.vectorizer.transform(q_texts)
        sim_matrix = q_matrix.dot(self.doc_matrix.T)

        for i, qid in enumerate(qids):
            scores = sim_matrix[i].toarray().flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results[qid] = [self.doc_ids[idx] for idx in top_indices]
        return results

# =====================================================================
# 2. OKAPI BM25 PROBABILISTIC MODEL
# =====================================================================
class BM25Retriever:
    def __init__(self, corpus: Dict[str, Dict[str, str]], cache_path: str = "data/bm25_index.pkl"):
        self.doc_ids = list(corpus.keys())
        self.cache_path = cache_path

        if os.path.exists(cache_path):
            print(f"Loading cached BM25 index from {cache_path}...")
            with open(cache_path, "rb") as f:
                self.bm25 = pickle.load(f)
        else:
            print("⚡ Tokenizing corpus with financial preprocessing & stemming for BM25...")
            tokenized_corpus = []
            for did in self.doc_ids:
                full_text = f"{corpus[did]['title']} {corpus[did]['text']}".strip()
                tokenized_corpus.append(preprocess_financial_text(full_text, apply_stemming=True))
                
            print(" Building BM25Okapi index (k1=1.5, b=0.75)...")
            self.bm25 = BM25Okapi(tokenized_corpus)
            with open(cache_path, "wb") as f:
                pickle.dump(self.bm25, f)
        print(" BM25 model ready.")

    def retrieve(self, query: str, top_k: int = 100) -> List[Tuple[str, float]]:
        q_tokens = preprocess_financial_text(query, apply_stemming=True)
        scores = self.bm25.get_scores(q_tokens)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self.doc_ids[i], float(scores[i])) for i in top_indices]

    def batch_retrieve(self, queries: Dict[str, str], top_k: int = 100) -> Dict[str, List[str]]:
        results = {}
        for qid, q_text in queries.items():
            ranked = self.retrieve(q_text, top_k=top_k)
            results[qid] = [did for did, _ in ranked]
        return results

# =====================================================================
# 3. SENTENCE TRANSFORMER (DENSE SEMANTIC MODEL)
# =====================================================================
class DenseRetriever:
    def __init__(
        self, 
        corpus: Dict[str, Dict[str, str]], 
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        cache_path: str = "data/dense_embeddings.npy",
        device: str = "cpu"
    ):
        self.doc_ids = list(corpus.keys())
        self.device = device
        self.cache_path = cache_path
        
        print(f"🧠 Loading Sentence Transformer: {model_name}...")
        self.model = SentenceTransformer(model_name, device=device)
        
        if os.path.exists(cache_path):
            print(f" Loading cached dense embeddings from {cache_path}...")
            self.embeddings = np.load(cache_path)
        else:
            print(" Encoding 57k documents into 384-dim dense vectors...")
            texts = [f"{corpus[did]['title']} {corpus[did]['text']}".strip() for did in self.doc_ids]
            self.embeddings = self.model.encode(
                texts, 
                batch_size=128, 
                show_progress_bar=True, 
                normalize_embeddings=True,
                device=device
            ).astype(np.float32)
            np.save(cache_path, self.embeddings)
            print(f" Dense embeddings saved to {cache_path}!")
        print(" Dense Retriever ready.")

    def retrieve(self, query: str, top_k: int = 100) -> List[Tuple[str, float]]:
        q_emb = self.model.encode([query], normalize_embeddings=True, device=self.device)[0]
        cos_scores = np.dot(self.embeddings, q_emb)
        top_indices = np.argsort(cos_scores)[::-1][:top_k]
        return [(self.doc_ids[i], float(cos_scores[i])) for i in top_indices]

    def batch_retrieve(self, queries: Dict[str, str], top_k: int = 100) -> Dict[str, List[str]]:
        qids = list(queries.keys())
        q_texts = [queries[qid] for qid in qids]
        
        print("Encoding test queries...")
        q_embs = self.model.encode(q_texts, normalize_embeddings=True, batch_size=64, device=self.device)
        sim_matrix = np.dot(q_embs, self.embeddings.T)

        results = {}
        for i, qid in enumerate(qids):
            top_indices = np.argsort(sim_matrix[i])[::-1][:top_k]
            results[qid] = [self.doc_ids[idx] for idx in top_indices]
        return results

# =====================================================================
# 4. HYBRID RECIPROCAL RANK FUSION (RRF)
# =====================================================================
def reciprocal_rank_fusion(
    rankings_list: List[List[str]], 
    k_rrf: int = 60, 
    top_k: int = 100
) -> List[str]:
    """
    Cormack et al. (2009) Reciprocal Rank Fusion:
    RRF_Score(d) = sum_{m in M} (1 / (k + rank_m(d)))
    """
    rrf_scores = defaultdict(float)
    for ranked_docs in rankings_list:
        for rank, did in enumerate(ranked_docs, start=1):
            rrf_scores[did] += 1.0 / (k_rrf + rank)
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return [did for did, _ in sorted_docs[:top_k]]

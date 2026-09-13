import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

_model = None
_index = None

def _load():
    global _model, _index
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    if _index is None:
        with open("data/retrieval_index.pkl", "rb") as f:
            _index = pickle.load(f)
    return _model, _index

def cosine_sim(query_vec, matrix):
    query_norm = query_vec / np.linalg.norm(query_vec)
    matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix_norm @ query_norm

def retrieve_similar(customer_text, top_k=3):
    model, index = _load()
    query_vec = model.encode([customer_text])[0]

    sims = cosine_sim(query_vec, index["embeddings"])
    top_indices = np.argsort(sims)[::-1][:top_k]

    results = []
    for i in top_indices:
        results.append({
            "customer_text": index["customer_texts"][i],
            "brand_reply": index["brand_replies"][i],
            "similarity": float(sims[i]),
        })
    return results

if __name__ == "__main__":
    test_query = "app keeps crashing when I try to shuffle my playlist"
    results = retrieve_similar(test_query, top_k=3)

    print(f"Query: {test_query}\n")
    for r in results:
        print(f"[sim={r['similarity']:.3f}] Customer: {r['customer_text']}")
        print(f"           Brand replied: {r['brand_reply']}\n")
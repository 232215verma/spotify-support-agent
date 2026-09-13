import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

def build_index(input_path="data/pairs_spotify.csv", output_path="data/retrieval_index.pkl"):
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["customer_text", "brand_reply"]).reset_index(drop=True)
    
    print(f"Building embeddings for {len(df)} customer messages...")
    
    model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, good enough for this
    embeddings = model.encode(
        df["customer_text"].tolist(),
        show_progress_bar=True,
        batch_size=64,
    )
    
    with open(output_path, "wb") as f:
        pickle.dump({
            "embeddings": embeddings,
            "customer_texts": df["customer_text"].tolist(),
            "brand_replies": df["brand_reply"].tolist(),
        }, f)
    
    print(f"Saved index to {output_path}")

if __name__ == "__main__":
    build_index()
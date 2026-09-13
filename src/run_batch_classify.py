import pandas as pd
from classify_intent import classify
from tqdm import tqdm
import time

def run_batch(input_path="data/pairs_spotify.csv", n=30, seed=7):
    df = pd.read_csv(input_path)
    sample = df.sample(n=n, random_state=seed).reset_index(drop=True)
    
    results = []
    for _, row in tqdm(sample.iterrows(), total=len(sample), desc="Classifying"):
        result = classify(row["customer_text"])
        results.append({
            "customer_text": row["customer_text"],
            "predicted_intent": result["intent"],
            "confidence": result.get("confidence", None),
            "reasoning": result.get("reasoning", ""),
        })
        time.sleep(0.3)  # be nice to the free-tier rate limit
    
    out = pd.DataFrame(results)
    out.to_csv("data/batch_classification_sample.csv", index=False)
    print(f"\nSaved {len(out)} classifications to data/batch_classification_sample.csv")
    
    print("\nIntent distribution:")
    print(out["predicted_intent"].value_counts())

if __name__ == "__main__":
    run_batch(n=30)
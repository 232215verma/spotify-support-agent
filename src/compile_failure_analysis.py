import pandas as pd

def compile_failures():
    # Load all our analysis artifacts
    misclassified = pd.read_csv("data/misclassified_examples.csv", encoding="utf-8-sig")
    
    print("="*70)
    print("SAMPLE MISCLASSIFICATIONS (for manual pattern review)")
    print("="*70)
    print(misclassified[["customer_text", "true_intent", "predicted_intent"]].head(20).to_string())

if __name__ == "__main__":
    compile_failures()
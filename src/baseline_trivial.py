import pandas as pd

def trivial_baseline(golden_path="data/golden_eval_final.csv"):
    df = pd.read_csv(golden_path, encoding="utf-8-sig")
    
    most_common_intent = df["true_intent"].value_counts().idxmax()
    print(f"Most common intent in golden set: {most_common_intent}")
    
    df["predicted_intent"] = most_common_intent
    accuracy = (df["true_intent"] == df["predicted_intent"]).mean()
    
    print(f"Trivial baseline accuracy (always predict '{most_common_intent}'): {accuracy:.1%}")
    return accuracy

if __name__ == "__main__":
    trivial_baseline()
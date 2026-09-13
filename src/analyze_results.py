import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

def analyze(results_path="data/eval_results_classification.csv"):
    df = pd.read_csv(results_path, encoding="utf-8-sig")
    
    y_true = df["true_intent"]
    y_pred = df["predicted_intent"]
    
    print("=" * 70)
    print("PER-INTENT CLASSIFICATION REPORT")
    print("=" * 70)
    print(classification_report(y_true, y_pred, zero_division=0))
    
    print("=" * 70)
    print("CONFUSION MATRIX (rows=true, cols=predicted)")
    print("=" * 70)
    labels = sorted(set(y_true) | set(y_pred))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)
    
    print("\n" + "=" * 70)
    print("CONFIDENCE ANALYSIS")
    print("=" * 70)
    df["is_correct"] = y_true == y_pred
    print("Average confidence when CORRECT:", df[df["is_correct"]]["predicted_confidence"].mean().round(3))
    print("Average confidence when WRONG:", df[~df["is_correct"]]["predicted_confidence"].mean().round(3))
    
    # Save confusion matrix and misclassified examples for the report
    cm_df.to_csv("data/confusion_matrix.csv")
    
    misclassified = df[~df["is_correct"]][["customer_text", "true_intent", "predicted_intent", "predicted_confidence"]]
    misclassified.to_csv("data/misclassified_examples.csv", index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(misclassified)} misclassified examples to data/misclassified_examples.csv")
    print("(useful for your failure analysis section)")

if __name__ == "__main__":
    analyze()
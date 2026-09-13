import pandas as pd
from escalate import decide_escalation

def eval_escalation(results_path="data/eval_results_classification.csv"):
    df = pd.read_csv(results_path, encoding="utf-8-sig")
    
    predicted_escalate = []
    reasons = []
    for _, row in df.iterrows():
        decision = decide_escalation(row["predicted_intent"], row["predicted_confidence"])
        predicted_escalate.append("yes" if decision["escalate"] else "no")
        reasons.append(decision["reason"])
    
    df["predicted_escalate"] = predicted_escalate
    df["escalation_reason"] = reasons
    
    # Normalize true_escalate to yes/no strings for comparison
    df["true_escalate"] = df["true_escalate"].astype(str).str.lower().str.strip()
    
    correct = (df["true_escalate"] == df["predicted_escalate"]).sum()
    total = len(df)
    accuracy = correct / total
    
    # Precision/recall framing: "yes" = positive class (escalate)
    tp = ((df["true_escalate"] == "yes") & (df["predicted_escalate"] == "yes")).sum()
    fp = ((df["true_escalate"] == "no") & (df["predicted_escalate"] == "yes")).sum()
    fn = ((df["true_escalate"] == "yes") & (df["predicted_escalate"] == "no")).sum()
    tn = ((df["true_escalate"] == "no") & (df["predicted_escalate"] == "no")).sum()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print(f"Escalation accuracy: {correct}/{total} = {accuracy:.1%}")
    print(f"\nConfusion breakdown:")
    print(f"  True Positive (correctly escalated):  {tp}")
    print(f"  False Positive (unnecessarily escalated): {fp}")
    print(f"  False Negative (missed escalation — RISKY): {fn}")
    print(f"  True Negative (correctly auto-handled): {tn}")
    print(f"\nPrecision (of escalated, how many needed it): {precision:.1%}")
    print(f"Recall (of those needing escalation, how many caught): {recall:.1%}")
    
    df.to_csv("data/eval_results_escalation.csv", index=False, encoding="utf-8-sig")
    
    missed = df[(df["true_escalate"] == "yes") & (df["predicted_escalate"] == "no")]
    if len(missed) > 0:
        print(f"\n{len(missed)} MISSED escalations (most important failure mode to review):")
        for _, row in missed.head(5).iterrows():
            print(f"  - {row['customer_text'][:80]}")

if __name__ == "__main__":
    eval_escalation()
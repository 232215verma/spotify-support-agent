import pandas as pd

# Simple rule-based keyword matcher — no LLM, no ML, just pattern matching
KEYWORD_RULES = {
    "billing_subscription": ["charge", "charged", "refund", "premium", "subscription", "trial", "student discount", "payment", "billed", "cancel"],
    "login_account_access": ["login", "log in", "password", "hacked", "sign in", "signed in", "access my account"],
    "downloads_offline": ["download", "downloaded", "offline"],
    "content_availability": ["available", "not on spotify", "remove", "removed", "missing", "country", "licensing"],
    "feature_request": ["please add", "would be great", "feature", "wish", "suggestion", "idea", "vote"],
    "resolved_positive": ["thank you", "thanks", "works now", "working now", "appreciate"],
    "playback_bug": ["crash", "bug", "shuffle", "skip", "won't play", "not working", "error"],
}

def classify_by_keyword(text):
    text_lower = text.lower()
    scores = {}
    for intent, keywords in KEYWORD_RULES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[intent] = score
    
    if not scores:
        return "feature_request"  # fallback to most common intent
    return max(scores, key=scores.get)

def keyword_baseline(golden_path="data/golden_eval_final.csv"):
    df = pd.read_csv(golden_path, encoding="utf-8-sig")
    df["predicted_intent"] = df["customer_text"].apply(classify_by_keyword)
    
    accuracy = (df["true_intent"] == df["predicted_intent"]).mean()
    print(f"Keyword baseline accuracy: {accuracy:.1%}")
    
    df.to_csv("data/baseline_keyword_results.csv", index=False, encoding="utf-8-sig")
    return accuracy

if __name__ == "__main__":
    keyword_baseline()
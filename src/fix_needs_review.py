import pandas as pd

fixes = {
    455632: ("billing_subscription", "yes"),   # £14.99 charge dispute
    471651: ("login_account_access", "yes"),    # auto logins stopped working
    338735: ("downloads_offline", "yes"),       # offline files bug, reinstall every 2 months
}

df = pd.read_csv("data/golden_eval_final.csv", encoding="utf-8-sig")

for tweet_id, (intent, escalate) in fixes.items():
    mask = df["customer_tweet_id"] == tweet_id
    df.loc[mask, "true_intent"] = intent
    df.loc[mask, "true_escalate"] = escalate

df.to_csv("data/golden_eval_final.csv", index=False, encoding="utf-8-sig")
print("Fixed. Remaining NEEDS_REVIEW count:", (df["true_intent"] == "NEEDS_REVIEW").sum())
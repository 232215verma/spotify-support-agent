import pandas as pd

def build_golden_sample(input_path="data/pairs_spotify.csv", n_total=200, seed=99):
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["customer_text"]).reset_index(drop=True)
    
    # We don't have true labels yet, so we take a random sample first,
    # then you'll hand-label the intent column yourself while reading.
    # To roughly stratify by length/type variety, we sample across different
    # text-length buckets so short and long messages both get representation.
    df["text_len"] = df["customer_text"].str.len()
    df["len_bucket"] = pd.qcut(df["text_len"], q=4, labels=["short", "medium", "long", "very_long"])
    
    per_bucket = n_total // 4
    sample = df.groupby("len_bucket", group_keys=False, observed=True).apply(
        lambda x: x.sample(n=min(per_bucket, len(x)), random_state=seed)
    ).reset_index(drop=True)
    
    sample = sample[["customer_text", "brand_reply", "customer_tweet_id", "reply_tweet_id"]]
    sample["true_intent"] = ""
    sample["true_escalate"] = ""  # you'll fill: yes/no
    sample["notes"] = ""
    
    sample.to_csv("data/golden_eval_raw.csv", index=False)
    print(f"Saved {len(sample)} examples to data/golden_eval_raw.csv")
    print("\nNow open this in Excel and fill in:")
    print("  - true_intent: one of the 7 intent names")
    print("  - true_escalate: yes/no (would a human need to handle this?)")
    print("  - notes: anything unusual, ambiguous, or worth flagging")

if __name__ == "__main__":
    build_golden_sample(n_total=200)
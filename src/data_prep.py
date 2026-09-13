import pandas as pd

def load_raw(path="data/twcs/twcs.csv", nrows=None):
    df = pd.read_csv(path, nrows=nrows)
    return df

def top_brands(df, n=20):
    """Brand accounts have inbound=False (they're the company, not customer)."""
    brands = df[df["inbound"] == False]["author_id"].value_counts()
    return brands.head(n)

def build_pairs(df, brand_handle):
    """Pair each brand reply with the customer message it replied to."""
    inbound = df[df["inbound"] == True].set_index("tweet_id")
    brand_replies = df[(df["inbound"] == False) & (df["author_id"] == brand_handle)]

    pairs = []
    for _, reply in brand_replies.iterrows():
        parent_id = reply["in_response_to_tweet_id"]
        if pd.isna(parent_id):
            continue
        parent_id = int(parent_id)
        if parent_id in inbound.index:
            customer_msg = inbound.loc[parent_id]
            pairs.append({
                "customer_text": customer_msg["text"],
                "brand_reply": reply["text"],
                "customer_tweet_id": parent_id,
                "reply_tweet_id": reply["tweet_id"]
            })
    return pd.DataFrame(pairs)

def get_thread_context(df, tweet_id, max_turns=4):
    """Walk backwards through the reply chain to reconstruct prior conversation turns."""
    all_tweets = df.set_index("tweet_id")
    thread = []
    current_id = tweet_id
    depth = 0

    while depth < max_turns:
        if current_id not in all_tweets.index:
            break
        row = all_tweets.loc[current_id]
        speaker = "customer" if row["inbound"] else "brand"
        thread.append({"speaker": speaker, "text": row["text"]})

        parent_id = row["in_response_to_tweet_id"]
        if pd.isna(parent_id):
            break
        current_id = int(parent_id)
        depth += 1

    thread.reverse()  # oldest first
    return thread

if __name__ == "__main__":
    df = load_raw()
    print(f"Loaded {len(df)} total rows")

    pairs = build_pairs(df, brand_handle="SpotifyCares")
    print(f"Found {len(pairs)} customer-brand message pairs for SpotifyCares")

    pairs.to_csv("data/pairs_spotify.csv", index=False)
    print("Saved to data/pairs_spotify.csv")
import pandas as pd
from data_prep import load_raw, get_thread_context
from classify_intent import classify

df = load_raw()

# The problematic tweet IDs from our earlier batch test (device-info fragments)
test_tweet_ids = {
    "iPhone 6 ios11.1.1 latest Spotify app": None,  # we'll search for it
}

# Let's just re-fetch by searching text since we don't have exact IDs handy
problem_texts = [
    "iPhone 6 ios11.1.1 latest Spotify app",
    "Huawei p9 lite/android",
]

for text_snippet in problem_texts:
    match = df[df["text"].str.contains(text_snippet, case=False, na=False, regex=False)]
    if len(match) == 0:
        print(f"Not found: {text_snippet}")
        continue
    row = match.iloc[0]
    thread = get_thread_context(df, row["tweet_id"], max_turns=4)
    
    print(f"\n--- Message: {row['text']}")
    print(f"Thread context found: {len(thread)} turns")
    for t in thread:
        print(f"    [{t['speaker']}] {t['text'][:80]}")
    
    result = classify(row["text"], thread=thread)
    print(f"  → NEW Intent: {result['intent']} (confidence: {result.get('confidence')})")
    print(f"  → Reasoning: {result.get('reasoning')}")
import pandas as pd
from data_prep import load_raw, get_thread_context
from intents import INTENTS
from llm_client import call_llm
from tqdm import tqdm
import time
import json

FALLBACK_MODEL = "openai/gpt-oss-120b"  # different model = separate daily quota

def format_thread(thread):
    if not thread or len(thread) <= 1:
        return None
    lines = []
    for turn in thread[:-1]:
        lines.append(f"{turn['speaker']}: {turn['text']}")
    return "\n".join(lines)

def classify_with_fallback(customer_text, thread=None):
    intent_list = "\n".join([f"- {name}: {desc}" for name, desc in INTENTS.items()])
    context_block = ""
    prior_context = format_thread(thread) if thread else None
    if prior_context:
        context_block = f"\nPrior conversation context (for reference only, classify the LATEST message):\n{prior_context}\n"

    prompt = f"""You are classifying a customer support message sent to Spotify's support team on Twitter.
{context_block}
Classify the message into EXACTLY ONE of these intents:

{intent_list}

Customer message to classify:
"{customer_text}"

Respond with ONLY valid JSON in this exact format, nothing else:
{{"intent": "<intent_name>", "confidence": <0.0 to 1.0>, "reasoning": "<one short sentence>"}}
"""
    raw = call_llm(prompt, model=FALLBACK_MODEL)
    try:
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"intent": "unknown", "confidence": 0.0, "reasoning": "parse_error"}

def retry_unknown(results_path="data/eval_results_classification.csv"):
    df = pd.read_csv(results_path, encoding="utf-8-sig")
    unknown_mask = df["predicted_intent"] == "unknown"
    n_unknown = unknown_mask.sum()
    print(f"Found {n_unknown} rows to retry using {FALLBACK_MODEL}")

    if n_unknown == 0:
        print("Nothing to retry!")
        return

    df_full = load_raw()

    for idx in tqdm(df[unknown_mask].index, desc="Retrying"):
        row = df.loc[idx]
        thread = get_thread_context(df_full, row["customer_tweet_id"], max_turns=4)
        result = classify_with_fallback(row["customer_text"], thread=thread)
        df.loc[idx, "predicted_intent"] = result.get("intent", "unknown")
        df.loc[idx, "predicted_confidence"] = result.get("confidence", 0.0)
        time.sleep(0.5)

    df.to_csv(results_path, index=False, encoding="utf-8-sig")
    still_unknown = (df["predicted_intent"] == "unknown").sum()
    print(f"\nDone. Still unknown: {still_unknown}")

if __name__ == "__main__":
    retry_unknown()
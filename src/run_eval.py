import pandas as pd
import argparse
from classify_intent import classify
from data_prep import load_raw, get_thread_context
from tqdm import tqdm
import time
import os

def run_classification_eval(golden_path="data/golden_eval_final.csv", use_context=True, n=None, seed=42):
    golden = pd.read_csv(golden_path, encoding="utf-8-sig")

    if n is not None and n < len(golden):
        golden = golden.sample(n=n, random_state=seed).reset_index(drop=True)
        print(f"Running on a subsample of {n} examples (use --n 200 or omit --n for the full set)")
    else:
        print(f"Running on the full golden set ({len(golden)} examples)")

    df_full = None
    if use_context:
        if os.path.exists("data/twcs/twcs.csv"):
            print("Loading full dataset for thread context...")
            df_full = load_raw()
        else:
            print("NOTE: data/twcs/twcs.csv not found (raw dataset not downloaded).")
            print("Running WITHOUT thread context — see 'Full Pipeline' section in README to enable it.")

    predictions = []
    confidences = []

    for _, row in tqdm(golden.iterrows(), total=len(golden), desc="Classifying golden set"):
        thread = None
        if df_full is not None:
            thread = get_thread_context(df_full, row["customer_tweet_id"], max_turns=4)

        result = classify(row["customer_text"], thread=thread)
        predictions.append(result.get("intent", "unknown"))
        confidences.append(result.get("confidence", 0.0))
        time.sleep(0.3)

    golden["predicted_intent"] = predictions
    golden["predicted_confidence"] = confidences

    output_path = "data/eval_results_classification.csv" if n is None else f"data/eval_results_classification_n{n}.csv"
    golden.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nSaved results to {output_path}")

    return golden

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run intent classification eval on the golden set.")
    parser.add_argument("--n", type=int, default=None, help="Subsample size for a faster run (e.g. --n 30). Omit for the full 200-example set.")
    args = parser.parse_args()

    results = run_classification_eval(n=args.n)

    correct = (results["true_intent"] == results["predicted_intent"]).sum()
    total = len(results)
    accuracy = correct / total
    print(f"\nOverall accuracy: {correct}/{total} = {accuracy:.1%}")
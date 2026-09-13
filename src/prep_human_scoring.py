import pandas as pd

def prep_human_scoring(input_path="data/replies_judged.csv", n=20, seed=5):
    df = pd.read_csv(input_path, encoding="utf-8-sig")
    sample = df.sample(n=n, random_state=seed).reset_index(drop=True)
    
    # Keep only what a human needs to see — hide the LLM judge's scores so you're not biased
    human_sheet = sample[["customer_text", "drafted_reply"]].copy()
    human_sheet["human_overall_score"] = ""  # you'll fill this: 1-5
    
    human_sheet.to_csv("data/human_scoring_sheet.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(human_sheet)} examples to data/human_scoring_sheet.csv")
    print("Open in Excel, read customer_text + drafted_reply, and score 'human_overall_score' 1-5:")
    print("  5 = ready to send as-is")
    print("  4 = good, minor tweak needed")
    print("  3 = okay but needs real edits")
    print("  2 = poor, mostly needs rewriting")
    print("  1 = unusable/wrong")

if __name__ == "__main__":
    prep_human_scoring(n=20)
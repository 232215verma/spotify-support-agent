import pandas as pd
from draft_reply import draft_reply
from tqdm import tqdm
import time

def generate_sample(golden_path="data/golden_eval_final.csv", n=40, seed=11):
    df = pd.read_csv(golden_path, encoding="utf-8-sig")
    sample = df.sample(n=n, random_state=seed).reset_index(drop=True)
    
    drafted_replies = []
    grounded_on = []
    
    for _, row in tqdm(sample.iterrows(), total=len(sample), desc="Drafting replies"):
        result = draft_reply(row["customer_text"], intent=row["true_intent"])
        drafted_replies.append(result.get("reply", ""))
        grounded_on.append(result.get("grounded_on", ""))
        time.sleep(0.5)
    
    sample["drafted_reply"] = drafted_replies
    sample["grounded_on"] = grounded_on
    
    sample.to_csv("data/replies_for_judging.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(sample)} drafted replies to data/replies_for_judging.csv")

if __name__ == "__main__":
    generate_sample(n=40)
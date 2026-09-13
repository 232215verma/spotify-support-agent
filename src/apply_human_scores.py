import pandas as pd

scores = [5, 4, 5, 4, 3, 5, 5, 4, 4, 5, 4, 5, 3, 5, 4, 3, 2]

df = pd.read_csv("data/human_scoring_sheet.csv", encoding="utf-8-sig")
df["human_overall_score"] = df["human_overall_score"].astype(object)

for i, score in enumerate(scores):
    df.loc[i, "human_overall_score"] = score

df.loc[16, "human_overall_score"] = "SKIP_CORRUPTED"
df.loc[17, "human_overall_score"] = 5
df.loc[18, "human_overall_score"] = 5
df.loc[19, "human_overall_score"] = 4

df.to_csv("data/human_scoring_sheet.csv", index=False, encoding="utf-8-sig")

print("Applied. Current state:")
print(df[["customer_text", "human_overall_score"]].to_string())
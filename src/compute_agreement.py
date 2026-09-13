import pandas as pd
from scipy.stats import pearsonr, spearmanr

def compute_agreement():
    human = pd.read_csv("data/human_scoring_sheet.csv", encoding="utf-8-sig")
    judged = pd.read_csv("data/replies_judged.csv", encoding="utf-8-sig")

    merged = human.merge(
        judged[["customer_text", "judge_overall"]],
        on="customer_text",
        how="left"
    )

    merged = merged[merged["human_overall_score"] != "SKIP_CORRUPTED"].copy()
    merged = merged[merged["judge_overall"] > 0].copy()
    merged["human_overall_score"] = merged["human_overall_score"].astype(int)

    print(f"Comparing {len(merged)} examples (excluded corrupted ones)")
    print(merged[["customer_text", "human_overall_score", "judge_overall"]].to_string())

    exact_match = (merged["human_overall_score"] == merged["judge_overall"]).mean()
    within_1 = (abs(merged["human_overall_score"] - merged["judge_overall"]) <= 1).mean()

    pearson_corr, pearson_p = pearsonr(merged["human_overall_score"], merged["judge_overall"])
    spearman_corr, spearman_p = spearmanr(merged["human_overall_score"], merged["judge_overall"])

    print("AGREEMENT METRICS")
    print(f"Exact match rate: {exact_match:.1%}")
    print(f"Within +/-1 point: {within_1:.1%}")
    print(f"Pearson correlation: {pearson_corr:.3f} (p={pearson_p:.3f})")
    print(f"Spearman correlation: {spearman_corr:.3f} (p={spearman_p:.3f})")

    merged.to_csv("data/agreement_analysis.csv", index=False, encoding="utf-8-sig")


compute_agreement()
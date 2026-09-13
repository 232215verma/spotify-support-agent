import pandas as pd

# Corrections found during review, keyed by customer_tweet_id (unique, safe to match on)
corrections = {
    974531: ("feature_request", "no"),
    2580687: ("content_availability", "no"),
    2038900: ("login_account_access", "yes"),
    917346: ("playback_bug", "no"),
    2932360: ("resolved_positive", "no"),
    2275376: ("resolved_positive", "no"),
    2981101: ("billing_subscription", "yes"),
    2912445: ("playback_bug", "yes"),
    812816: ("content_availability", "no"),
    1977638: ("playback_bug", "no"),
    1421482: ("feature_request", "no"),
    2572256: ("playback_bug", "no"),
    2145967: ("feature_request", "no"),
    1933854: ("content_availability", "no"),
    2603342: ("playback_bug", "yes"),
    186494: ("playback_bug", "yes"),
    2947627: ("login_account_access", "yes"),
    2056255: ("playback_bug", "yes"),
    783596: ("login_account_access", "yes"),
    482468: ("billing_subscription", "yes"),
    2154913: ("content_availability", "no"),
    2259633: ("downloads_offline", "yes"),
    2153126: ("playback_bug", "no"),
    2304270: ("billing_subscription", "yes"),
    1703341: ("downloads_offline", "no"),
    1715259: ("playback_bug", "no"),
    1476014: ("billing_subscription", "yes"),
    562466: ("feature_request", "no"),
    2175444: ("feature_request", "no"),
    1317756: ("billing_subscription", "yes"),
    444533: ("feature_request", "yes"),
    113864: ("login_account_access", "yes"),
    190106: ("playback_bug", "no"),
    1666499: ("billing_subscription", "yes"),
    158956: ("content_availability", "no"),
    2511292: ("playback_bug", "no"),
    2349676: ("content_availability", "no"),
    51767: ("playback_bug", "no"),
    2947644: ("billing_subscription", "no"),
    1429270: ("billing_subscription", "yes"),
    2289896: ("content_availability", "no"),
    653078: ("downloads_offline", "no"),
    2251390: ("content_availability", "no"),
    1963830: ("login_account_access", "yes"),
    2076426: ("billing_subscription", "yes"),
    1713302: ("billing_subscription", "yes"),
    2733024: ("feature_request", "no"),
    1807112: ("playback_bug", "yes"),
    2128543: ("feature_request", "no"),
    1742689: ("feature_request", "no"),
    560958: ("feature_request", "no"),
    2674454: ("playback_bug", "no"),
}

df = pd.read_csv("data/golden_eval_draft.csv", encoding="utf-8")

applied = 0
for tweet_id, (intent, escalate) in corrections.items():
    mask = df["customer_tweet_id"] == tweet_id
    if mask.sum() == 1:
        df.loc[mask, "true_intent"] = intent
        df.loc[mask, "true_escalate"] = escalate
        df.loc[mask, "notes"] = "corrected during review"
        applied += 1
    else:
        print(f"WARNING: tweet_id {tweet_id} matched {mask.sum()} rows, expected 1")

df.to_csv("data/golden_eval_final.csv", index=False, encoding="utf-8-sig")
print(f"Applied {applied}/{len(corrections)} corrections")
print(f"Saved to data/golden_eval_final.csv")
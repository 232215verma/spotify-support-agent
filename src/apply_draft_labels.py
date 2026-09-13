import pandas as pd

# Draft labels — LLM-assisted first pass, in the same row order as your golden_eval_raw.csv
# IMPORTANT: review these yourself before using them as your final golden set.
# Mark anything you disagree with in the 'notes' column of the CSV.

draft_labels = [
    ("billing_subscription", "no"), ("login_account_access", "yes"), ("playback_bug", "yes"),
    ("resolved_positive", "no"), ("playback_bug", "no"), ("login_account_access", "yes"),
    ("login_account_access", "yes"), ("feature_request", "no"), ("downloads_offline", "yes"),
    ("feature_request", "no"), ("content_availability", "no"), ("playback_bug", "no"),
    ("playback_bug", "no"), ("downloads_offline", "no"), ("login_account_access", "yes"),
    ("resolved_positive", "no"), ("login_account_access", "yes"), ("playback_bug", "no"),
    ("downloads_offline", "yes"), ("resolved_positive", "no"), ("playback_bug", "no"),
    ("billing_subscription", "no"), ("resolved_positive", "no"), ("billing_subscription", "no"),
    ("login_account_access", "yes"), ("content_availability", "no"), ("login_account_access", "yes"),
    ("feature_request", "no"), ("billing_subscription", "no"), ("playback_bug", "no"),
    ("content_availability", "no"), ("content_availability", "yes"), ("resolved_positive", "no"),
    ("playback_bug", "yes"), ("login_account_access", "yes"), ("resolved_positive", "no"),
    ("feature_request", "no"), ("resolved_positive", "no"), ("billing_subscription", "yes"),
    ("content_availability", "no"), ("billing_subscription", "no"), ("feature_request", "no"),
    ("resolved_positive", "no"), ("playback_bug", "no"), ("feature_request", "no"),
    ("resolved_positive", "no"), ("playback_bug", "yes"), ("playback_bug", "no"),
    ("playback_bug", "no"), ("feature_request", "no"), ("downloads_offline", "no"),
    ("feature_request", "no"), ("feature_request", "no"), ("feature_request", "no"),
    ("downloads_offline", "no"), ("feature_request", "no"), ("feature_request", "no"),
    ("login_account_access", "yes"), ("content_availability", "no"), ("billing_subscription", "yes"),
    ("content_availability", "no"), ("billing_subscription", "no"), ("playback_bug", "no"),
    ("billing_subscription", "yes"), ("feature_request", "no"), ("downloads_offline", "yes"),
    ("content_availability", "yes"), ("playback_bug", "no"), ("content_availability", "no"),
    ("billing_subscription", "yes"), ("billing_subscription", "yes"), ("playback_bug", "no"),
    ("login_account_access", "yes"), ("feature_request", "no"), ("content_availability", "no"),
    ("playback_bug", "no"), ("playback_bug", "yes"), ("feature_request", "no"),
    ("feature_request", "no"), ("feature_request", "no"), ("billing_subscription", "no"),
    ("login_account_access", "yes"), ("feature_request", "no"), ("resolved_positive", "no"),
    ("content_availability", "no"), ("billing_subscription", "yes"), ("playback_bug", "no"),
    ("playback_bug", "yes"), ("login_account_access", "no"), ("feature_request", "no"),
    ("login_account_access", "yes"), ("playback_bug", "no"), ("playback_bug", "yes"),
    ("content_availability", "no"), ("resolved_positive", "no"), ("feature_request", "no"),
    ("feature_request", "no"), ("downloads_offline", "no"), ("playback_bug", "no"),
    ("login_account_access", "yes"), ("playback_bug", "yes"), ("feature_request", "no"),
    ("billing_subscription", "yes"), ("resolved_positive", "no"), ("billing_subscription", "yes"),
    ("playback_bug", "yes"), ("playback_bug", "no"), ("playback_bug", "no"),
    ("feature_request", "no"), ("login_account_access", "yes"), ("login_account_access", "yes"),
    ("feature_request", "no"), ("downloads_offline", "yes"), ("playback_bug", "no"),
    ("billing_subscription", "yes"), ("feature_request", "no"), ("downloads_offline", "yes"),
    ("playback_bug", "no"), ("billing_subscription", "yes"), ("resolved_positive", "no"),
    ("login_account_access", "yes"), ("login_account_access", "yes"), ("feature_request", "no"),
    ("resolved_positive", "no"), ("content_availability", "no"), ("billing_subscription", "yes"),
    ("playback_bug", "no"), ("playback_bug", "yes"), ("content_availability", "no"),
    ("resolved_positive", "no"), ("resolved_positive", "no"), ("billing_subscription", "yes"),
    ("playback_bug", "yes"), ("content_availability", "yes"), ("playback_bug", "no"),
    ("resolved_positive", "no"), ("playback_bug", "no"), ("feature_request", "no"),
    ("feature_request", "no"), ("playback_bug", "yes"), ("playback_bug", "yes"),
    ("login_account_access", "yes"), ("playback_bug", "no"), ("playback_bug", "yes"),
    ("feature_request", "no"), ("playback_bug", "yes"), ("content_availability", "no"),
    ("login_account_access", "yes"), ("billing_subscription", "yes"), ("content_availability", "no"),
    ("downloads_offline", "yes"), ("playback_bug", "no"), ("billing_subscription", "yes"),
    ("resolved_positive", "no"), ("billing_subscription", "no"), ("downloads_offline", "no"),
    ("playback_bug", "yes"), ("billing_subscription", "yes"), ("feature_request", "no"),
    ("feature_request", "no"), ("billing_subscription", "yes"), ("billing_subscription", "no"),
    ("feature_request", "no"), ("login_account_access", "yes"), ("feature_request", "no"),
    ("playback_bug", "no"), ("billing_subscription", "yes"), ("content_availability", "no"),
    ("playback_bug", "no"), ("feature_request", "no"), ("content_availability", "no"),
    ("billing_subscription", "yes"), ("content_availability", "no"), ("billing_subscription", "no"),
    ("feature_request", "no"), ("billing_subscription", "yes"), ("login_account_access", "yes"),
    ("content_availability", "no"), ("billing_subscription", "yes"), ("login_account_access", "yes"),
    ("billing_subscription", "yes"), ("billing_subscription", "yes"), ("feature_request", "no"),
    ("content_availability", "no"), ("feature_request", "no"), ("playback_bug", "yes"),
    ("downloads_offline", "no"), ("feature_request", "no"), ("feature_request", "no"),
    ("feature_request", "no"), ("playback_bug", "yes"), ("feature_request", "no"),
    ("playback_bug", "no"), ("playback_bug", "no"), ("billing_subscription", "yes"),
    ("login_account_access", "yes"), ("playback_bug", "no"),
]

df = pd.read_csv("data/golden_eval_raw.csv")

n_rows = len(df)
n_labels = len(draft_labels)

if n_labels < n_rows:
    # pad missing rows with a clear placeholder so you know exactly which ones to hand-label yourself
    missing = n_rows - n_labels
    draft_labels = draft_labels + [("NEEDS_REVIEW", "NEEDS_REVIEW")] * missing
    print(f"Padded {missing} missing rows with NEEDS_REVIEW placeholder — label these yourself.")
elif n_labels > n_rows:
    draft_labels = draft_labels[:n_rows]
    print(f"Trimmed {n_labels - n_rows} extra labels to match row count.")

df["true_intent"] = [x[0] for x in draft_labels]
df["true_escalate"] = [x[1] for x in draft_labels]
df["notes"] = "LLM-DRAFT — please review"
df.to_csv("data/golden_eval_draft.csv", index=False)
print(f"Saved {len(df)} rows to data/golden_eval_draft.csv — REVIEW BEFORE USING AS FINAL GOLDEN SET")
print(f"Rows marked NEEDS_REVIEW: {(df['true_intent'] == 'NEEDS_REVIEW').sum()}")
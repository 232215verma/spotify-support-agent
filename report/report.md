# SpotifyCares AI Support Agent — Technical Report

## 1. Problem Framing

SpotifyCares was selected over broader-scope brands (e.g. AmazonHelp) because its issue space is naturally bounded — playback, billing, content availability, and account access — which made it feasible to derive a clean, data-driven taxonomy rather than an assumed one.

**Definition of "good" for this system:**

- *Classification* is correct if it captures the customer's underlying need closely enough to route the case appropriately, independent of exact phrasing.
- *A drafted reply* is good if it is relevant, on-brand in tone, and gives the customer a concrete next step — even if that step is "we've sent you a DM."
- *An escalation decision* is good if it prioritizes recall on security- and money-sensitive cases over precision. A missed escalation has direct customer-facing cost; an unnecessary one does not.

**Explicit scope decisions:**

- The system drafts replies and recommends escalation; it does not send replies autonomously. This reflects a human-in-the-loop design, consistent with how a support team would realistically deploy this.
- Classification uses single-turn intent detection with bounded (4-turn) backward thread context — not full multi-turn dialogue management.
- No model fine-tuning was performed. Given the assignment's time constraints, the system uses prompted LLM calls (Groq-hosted `openai/gpt-oss-20b` and `openai/gpt-oss-120b`) combined with retrieval-based grounding.
- Intents are single-label. Several failure cases (Section 4) indicate messages that genuinely span two intents; multi-label classification was out of scope for this iteration but is a clear next step.

**Intent taxonomy** (derived from manual review of ~300 real customer messages before any classification logic was written):

| Intent | Definition |
|---|---|
| `playback_bug` | Technical playback issues — shuffle, repeat, crashes, search failures |
| `login_account_access` | Login failures, password reset issues, hacked/compromised accounts |
| `billing_subscription` | Incorrect charges, premium activation issues, refunds, trials, discounts |
| `downloads_offline` | Downloaded/offline content issues, device download limits |
| `content_availability` | Missing songs/albums/artists due to licensing or regional unavailability |
| `feature_request` | Suggestions for new features or improvements |
| `resolved_positive` | Thank-you or confirmation messages requiring no action |

## 2. System Architecture

Each incoming message passes through four stages:

1. **Classify** — an LLM call assigns one of the 7 intents, incorporating up to 4 turns of backward thread context (reconstructed via the dataset's reply-chain IDs), and returns a confidence score.
2. **Retrieve** — a sentence-embedding index (`all-MiniLM-L6-v2`) over all 43,092 historical SpotifyCares customer-reply pairs surfaces the top-3 most similar resolved cases via cosine similarity.
3. **Draft** — a second LLM call generates a reply grounded in the pattern of the retrieved examples, not a verbatim copy.
4. **Escalate** — a decision rule combines classifier confidence with intent-specific defaults to determine auto-handle vs. escalate-to-human status, returning a stated reason.

## 3. Results vs. Baselines

Intent classification accuracy was measured on a 200-example hand-labeled golden set against two baselines:

| Approach | Accuracy |
|---|---|
| Trivial (always predict the most frequent intent, `playback_bug`) | 25.0% |
| Simple (keyword matching; no ML or LLM) | 37.5% |
| **Pipeline (LLM classification + retrieval + thread context)** | **75.0%** |

The pipeline outperforms the keyword baseline by ~2x and the trivial baseline by 3x. Section 5 addresses caveats on how this figure should be interpreted.

Per-intent performance was uneven:

| Intent | F1 |
|---|---|
| billing_subscription | 0.87 |
| resolved_positive | 0.82 |
| playback_bug | 0.78 |
| content_availability | 0.72 |
| downloads_offline | 0.70 |
| feature_request | 0.70 |
| login_account_access | 0.62 |

**Escalation decision performance:** 75.0% accuracy (150/200), 67.6% precision, 62.2% recall on the "needs escalation" class. The recall figure is the operationally significant one: **28 of 200 cases requiring human review were classified as safe to auto-handle**, representing the system's highest-risk failure mode — this is the metric that would materially affect a real deployment.

Classifier confidence correlates meaningfully with correctness: average confidence was 0.907 on correct predictions versus 0.746 on incorrect ones. This gap justifies the escalation logic's direct use of confidence as a signal, independent of the predicted intent label.

## 4. Failure Analysis

Five recurring failure patterns were identified from manual review of misclassified examples.

**1. Context-less fragments.** Short follow-up messages (device details, "Thanks just sent," "Yup, my home WiFi") carry minimal standalone signal. Example: *"@SpotifyCares Thanks just sent."* — labeled `login_account_access`, predicted `resolved_positive`. Even with 4-turn thread context, brief generic replies remain ambiguous. A longer context window or explicit low-information-message handling is a likely mitigation.

**2. `downloads_offline` boundary confusion with `feature_request`/`billing_subscription`.** Example: *"why is there a limit to how large my library can be"* — labeled `downloads_offline`, predicted `feature_request`. This reflects genuine taxonomy ambiguity: download-limit complaints are structurally phrased like feature requests or billing grievances.

**3. `login_account_access` over-triggering on generic thread closings.** Example: *"i'll try in a few days if i can for that."* — labeled `resolved_positive`, predicted `login_account_access`. Likely cause: prior thread turns involving login/DM discussion bias the classifier beyond the current message's actual content.

**4. `content_availability` vs. `playback_bug` keyword confusion.** Example: *"U guys fixed it once but its back"* (a recurring artist-page issue) — labeled `content_availability`, predicted `playback_bug`. Surface terms like "fixed" appear to pull classification toward playback issues regardless of underlying cause.

**5. `billing_subscription` misread as `feature_request`.** Example: *"we have premium family and cannot listen at the same time"* — labeled `billing_subscription`, predicted `feature_request`. Complaints about plan limitations are phrased similarly to feature suggestions.

**Synthesis:** the majority of errors stem from genuine ambiguity at taxonomy boundaries rather than the model failing to comprehend message content. This indicates the more effective fix is taxonomy refinement (finer-grained sub-categories, or multi-label support) rather than a larger or more capable model.

## 5. What Is Misleading About These Headline Numbers

Both headline figures — 75% classification accuracy and a 4.40/5 average reply-quality score — require qualification before being treated as reliable indicators of system quality.

**On the 75% accuracy figure:** the golden set was not built through fully independent human labeling. 197 of 200 labels originated as LLM-drafted suggestions, subsequently reviewed and corrected by hand; that review process caught a 26% error rate in the drafts. While the correction process is a legitimate and documented methodology, it means the resulting accuracy figure is anchored to a labeling process that started from the same class of model being evaluated. A fully independent, non-LLM-assisted labeling pass — the recommended next step — would provide a more defensible baseline and could shift this figure in either direction.

**On the 4.40/5 reply-quality score:** validation against 18 human-scored examples showed a weak, statistically non-significant negative correlation (Pearson r = -0.29, p = 0.24) and only 28% exact agreement with human ratings, though 83% fell within one point. This indicates the LLM-judge is not reliably tracking the same quality signal a human evaluator uses — it may be over-weighting tone and structural politeness relative to substantive correctness. **The 4.40/5 figure should not be cited as a standalone quality metric without this caveat; at the current sample size and agreement level, it is not a validated measure.**

**Additional context the headline numbers obscure:** the 75% accuracy figure conceals substantial per-intent variance (F1 range: 0.62–0.87), and the 62.2% escalation recall — arguably the most operationally consequential metric in this report — is not captured by the classification accuracy figure at all.

## 6. Next Steps With One Additional Week

- Construct a second, fully independent golden set with no LLM-assisted labeling, and use it to re-validate both the classification accuracy and judge-agreement figures.
- Redesign the LLM-judge rubric with concrete scoring anchors and mandatory reasoning prior to scoring; re-validate agreement. If correlation remains weak, reduce the judge to a coarse flag/no-flag signal rather than a 1–5 scale.
- Implement multi-label intent classification to address taxonomy-boundary failure modes identified in Section 4.
- Add a rule-based safety net for escalation (flagging terms such as "hacked," "dispute," "never signed up" regardless of classifier output) to reduce the 28 missed escalations identified in this evaluation.
- Test extended thread-context windows (6–8 turns vs. the current 4) to assess impact on context-less-fragment failures.
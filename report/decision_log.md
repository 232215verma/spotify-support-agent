# Decision Log

A record of non-obvious decisions made during this project, and the reasoning behind each.

1. **Chose SpotifyCares over higher-volume brands (e.g. AmazonHelp).** AmazonHelp had ~3x more data in the sample, but its issue space is too broad for a clean intent taxonomy in the available time. SpotifyCares' narrower, more homogeneous issue space made a rigorous evaluation feasible.

2. **Derived the intent taxonomy bottom-up from ~300 manually read messages**, rather than starting from an assumed category list. This surfaced categories (e.g. `downloads_offline` as distinct from general playback bugs) that would not have been obvious from intuition alone.

3. **Used single-label intents despite evidence of multi-intent messages.** Several failure cases (Section 4 of the report) genuinely span two categories. Multi-label classification was deferred to keep the evaluation harness tractable within the time available; this is flagged explicitly as a limitation rather than hidden.

4. **Added confidence-based escalation as a safety net, independent of intent-type defaults.** Initial escalation logic relied solely on intent type (e.g. always escalate billing). Testing showed low-confidence predictions were unreliable regardless of intent, so a confidence threshold (0.6) was added as an additional trigger. This is empirically justified: correct predictions averaged 0.907 confidence vs. 0.746 for incorrect ones.

5. **Incorporated bounded backward thread-context (4 turns) into classification**, after discovering that single-tweet classification systematically failed on context-dependent fragments (e.g. device-info replies to a prior troubleshooting question). This measurably improved confidence and accuracy on affected cases, though did not eliminate the failure mode entirely (see Failure Analysis, pattern 1).

6. **Used LLM-assisted draft labeling for the golden evaluation set, followed by full manual review.** Given the volume required (200 examples), fully manual labeling from scratch was time-prohibitive. The draft-then-review approach was chosen deliberately as a documented methodology, not as a shortcut — the review process caught a 26% correction rate, which is itself reported as a finding rather than concealed.

7. **Validated the LLM-as-judge against human-scored examples before trusting its output**, rather than reporting the judge's average score as a standalone metric. This surfaced a weak/negative correlation with human judgment, materially changing how the reply-quality metric should be interpreted and reported.

8. **Prioritized escalation recall over precision by design.** The system is intentionally biased toward escalating uncertain cases rather than risking an inadequate auto-handled response, reflecting the asymmetric cost of the two error types in a customer support context.

9. **Switched between two Groq-hosted models (`openai/gpt-oss-20b` and `openai/gpt-oss-120b`) during evaluation** due to free-tier daily token limits being reached on the primary model mid-evaluation. This was handled by routing only the affected retry calls to the secondary model, preserving the integrity of already-completed results rather than re-running the full evaluation.

10. **Excluded corrupted/parse-failed samples from agreement and accuracy calculations** (e.g. one LLM-judge response that failed JSON parsing) rather than imputing or guessing values, to avoid introducing artificial signal into a small validation sample.

11. **Kept reply drafting "always-on," even for escalated cases.** Rather than skipping reply generation when a case is flagged for escalation, the system still drafts a suggested reply — giving a human agent a starting point rather than a blank slate, while the escalation flag itself still routes the case for review.

12. **Used a small, fixed sample (n=40) for reply-quality judging and a subsample of that (n=18-20) for human-agreement validation**, rather than judging the full golden set. This kept API costs and evaluation time manageable while still providing statistically interpretable (if not highly powered) agreement evidence, as required by the assignment.

13. **Reported the escalation recall (62.2%) as the most operationally significant metric**, rather than leading with the higher-level classification accuracy (75%), because a missed escalation has direct customer-facing consequences that a classification error alone does not.

14. **Did not attempt to "fix" the LLM-judge's rubric mid-evaluation after observing weak agreement.** Re-tuning the judge after seeing disagreement with human scores would risk overfitting the judge to this specific validation sample. Instead, the weak agreement is reported as a finding, with judge redesign proposed as future work.
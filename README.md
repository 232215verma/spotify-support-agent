# SpotifyCares AI Support Agent

An AI customer support agent for SpotifyCares (built on the Kaggle "Customer Support on Twitter" dataset) that classifies customer messages, drafts grounded replies, and decides whether to auto-handle or escalate to a human.

Full report: [`report/report.md`](report/report.md)
Decision log: [`report/decision_log.md`](report/decision_log.md)

## Quick Reproduce (under 15 minutes)

This path uses the pre-built artifacts included in the repo (golden eval set, retrieval index) so you don't need to re-download the 3M-row dataset or rebuild embeddings from scratch.

### 1. Setup (2 min)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 2. Add your Groq API key (1 min)

Create a `.env` file in the repo root:
GROQ_API_KEY=PASTE YOUR OWN KEY

Free API keys are available at [console.groq.com](https://console.groq.com) — no payment required.

### 3. Run the eval on a small subsample (~1 min)

```bash
python src/run_eval.py --n 15
```

Verified runtime: 15 examples classified in ~26 seconds (plus ~30s to load the dataset for thread context). This reproduces the full pipeline (classification with retrieval + thread context) on a subsample and reports accuracy.

**Note:** thread-context uses the raw dataset (`data/twcs/twcs.csv`), which is gitignored due to size (500MB+). If it isn't present, the script automatically falls back to classifying without thread context (a small accuracy drop is expected — see "Full Pipeline" below to enable full context).

### 4. View pre-computed full results (instant, no API calls)

The full 200-example evaluation has already been run; results are included in the repo:

```bash
python src/analyze_results.py
python src/eval_escalation.py
python src/compute_agreement.py
```

These read from saved CSV files (`data/eval_results_classification.csv`, `data/replies_judged.csv`, `data/human_scoring_sheet.csv`) and print the full classification report, confusion matrix, escalation metrics, and judge-vs-human agreement analysis — no API calls needed.

## Headline Results

| Metric | Value |
|---|---|
| Classification accuracy (vs. trivial baseline 25.0% / keyword baseline 37.5%) | **75.0%** |
| Escalation decision accuracy | 75.0% |
| Escalation recall (needs-review cases correctly caught) | 62.2% |
| LLM-judge average reply quality | 4.40/5 (not independently validated — see caveat below) |
| LLM-judge vs. human agreement (Pearson r) | -0.29 (weak/negative) |

**Important:** see [`report/report.md`](report/report.md) Section 5 ("What Is Misleading About These Headline Numbers") before quoting the accuracy or reply-quality figures — both require context to interpret correctly.

## Full Pipeline (from scratch)

Not required for review; included for completeness / reproducibility of the full evaluation.

```bash
# 1. Download dataset (requires a Kaggle API token in ~/.kaggle/)
kaggle datasets download -d thoughtvector/customer-support-on-twitter -p data/
cd data && tar -xf customer-support-on-twitter.zip && cd ..

# 2. Extract SpotifyCares conversation pairs (~1 min)
python src/data_prep.py

# 3. Build retrieval embeddings over all 43k pairs (~11 min)
python src/build_retrieval_index.py

# 4. Run the full 200-example golden set evaluation (~14 min, uses API quota)
python src/run_eval.py

# 5. Generate and judge sample replies for quality evaluation (~10 min)
python src/generate_replies_for_judging.py
python src/llm_judge.py
python src/compute_agreement.py
```

## Repository Structure 
├── src/
│ │
│ ├── Core Pipeline
│ │ ├── data_prep.py # dataset loading, pair extraction, thread reconstruction
│ │ ├── llm_client.py # shared Groq API wrapper with retry logic
│ │ ├── intents.py # intent taxonomy + escalation defaults
│ │ ├── classify_intent.py # intent classification (with thread context)
│ │ ├── retrieve.py # embedding-based retrieval over historical replies
│ │ ├── draft_reply.py # grounded reply generation
│ │ ├── escalate.py # escalation decision logic
│ │ └── pipeline.py # end-to-end orchestration (classify → retrieve → draft → escalate)
│ │
│ ├── Evaluation Harness
│ │ ├── run_eval.py # runs classification pipeline on the golden set (supports --n for subsampling)
│ │ ├── analyze_results.py # classification metrics, confusion matrix, confidence analysis
│ │ ├── eval_escalation.py # escalation decision evaluation (precision/recall)
│ │ ├── generate_replies_for_judging.py # drafts replies for a reply-quality sample
│ │ ├── llm_judge.py # LLM-as-judge scoring of drafted replies
│ │ ├── compute_agreement.py # LLM-judge vs. human-rater agreement analysis
│ │ ├── baseline_trivial.py # trivial baseline (most-common-intent)
│ │ └── baseline_keyword.py # keyword-matching baseline
│ │
│ └── Golden Set Construction (one-time setup scripts)
│ ├── build_retrieval_index.py # builds the sentence-embedding index over all 43k pairs
│ ├── sample_for_labeling.py # samples messages for manual intent labeling
│ ├── build_golden_sample.py # builds the 200-example stratified golden sample
│ ├── apply_draft_labels.py # applies LLM-assisted draft labels (reviewed manually after)
│ └── prep_human_scoring.py # prepares the human-rater sheet for judge validation
│
├── data/ # golden eval set + evaluation results (raw dataset gitignored — see note)
│ ├── golden_eval_final.csv # 200-example hand-reviewed golden set
│ ├── eval_results_classification.csv # full classification eval results
│ ├── eval_results_escalation.csv # escalation eval results
│ ├── replies_judged.csv # LLM-judge scores on sampled replies
│ ├── human_scoring_sheet.csv # human ratings used for judge validation
│ ├── agreement_analysis.csv # judge-vs-human agreement data
│ ├── confusion_matrix.csv # intent confusion matrix
│ └── misclassified_examples.csv # failure cases used in the report's failure analysis
│
├── report/
│ ├── report.md # full technical report
│ └── decision_log.md # 14 non-obvious decisions + rationale
│
├── requirements.txt
├── .env # Groq API key (gitignored)
└── README.md  


**Note on `src/`:** the "Golden Set Construction" scripts were one-time setup steps (building the retrieval index, sampling and labeling the golden set) rather than part of the runtime pipeline — they're included for reproducibility and transparency about how the evaluation data was built, not because they'd be re-run in production.
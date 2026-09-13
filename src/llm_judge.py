from llm_client import call_llm
import pandas as pd
from tqdm import tqdm
import json
import time

def build_judge_prompt(customer_text, drafted_reply, brand_reply_actual):
    prompt = f"""You are evaluating the quality of an AI-drafted customer support reply for Spotify.

Customer message: "{customer_text}"

AI-drafted reply: "{drafted_reply}"

For reference, here is how Spotify's actual support team replied to this exact message (NOT necessarily perfect, just for context):
"{brand_reply_actual}"

Rate the AI-drafted reply on a 1-5 scale for each criterion:
- relevance: Does it directly address the customer's issue? (1=off-topic, 5=perfectly on-topic)
- tone: Does it match Spotify's friendly, concise support tone? (1=wrong tone, 5=perfect tone)
- actionability: Does it give the customer a clear next step or answer? (1=vague, 5=very clear)
- overall: Your overall quality judgment (1=unusable, 5=ready to send as-is)

Respond with ONLY valid JSON in this format:
{{"relevance": <1-5>, "tone": <1-5>, "actionability": <1-5>, "overall": <1-5>, "reasoning": "<one short sentence>"}}
"""
    return prompt

def judge_reply(customer_text, drafted_reply, brand_reply_actual):
    prompt = build_judge_prompt(customer_text, drafted_reply, brand_reply_actual)
    raw = call_llm(prompt, model="openai/gpt-oss-120b", max_tokens=300)
    try:
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"relevance": 0, "tone": 0, "actionability": 0, "overall": 0, "reasoning": "parse_error"}

def run_judge(input_path="data/replies_for_judging.csv"):
    df = pd.read_csv(input_path, encoding="utf-8-sig")
    
    relevance, tone, actionability, overall, reasoning = [], [], [], [], []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Judging replies"):
        result = judge_reply(row["customer_text"], row["drafted_reply"], row["brand_reply"])
        relevance.append(result.get("relevance", 0))
        tone.append(result.get("tone", 0))
        actionability.append(result.get("actionability", 0))
        overall.append(result.get("overall", 0))
        reasoning.append(result.get("reasoning", ""))
        time.sleep(0.5)
    
    df["judge_relevance"] = relevance
    df["judge_tone"] = tone
    df["judge_actionability"] = actionability
    df["judge_overall"] = overall
    df["judge_reasoning"] = reasoning
    
    df.to_csv("data/replies_judged.csv", index=False, encoding="utf-8-sig")
    print(f"\nSaved judged results to data/replies_judged.csv")
    print(f"\nAverage scores:")
    print(f"  Relevance: {df['judge_relevance'].mean():.2f}/5")
    print(f"  Tone: {df['judge_tone'].mean():.2f}/5")
    print(f"  Actionability: {df['judge_actionability'].mean():.2f}/5")
    print(f"  Overall: {df['judge_overall'].mean():.2f}/5")

if __name__ == "__main__":
    run_judge()
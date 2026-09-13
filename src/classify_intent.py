from llm_client import call_llm
from intents import INTENTS
import json

def format_thread(thread):
    if not thread or len(thread) <= 1:
        return None
    lines = []
    for turn in thread[:-1]:  # everything except the message we're classifying
        lines.append(f"{turn['speaker']}: {turn['text']}")
    return "\n".join(lines)

def build_classification_prompt(customer_text, thread=None):
    intent_list = "\n".join([f"- {name}: {desc}" for name, desc in INTENTS.items()])
    
    context_block = ""
    prior_context = format_thread(thread) if thread else None
    if prior_context:
        context_block = f"""
Prior conversation context (for reference only, classify the LATEST message):
{prior_context}
"""

    prompt = f"""You are classifying a customer support message sent to Spotify's support team on Twitter.
{context_block}
Classify the message into EXACTLY ONE of these intents:

{intent_list}

Customer message to classify:
"{customer_text}"

Respond with ONLY valid JSON in this exact format, nothing else:
{{"intent": "<intent_name>", "confidence": <0.0 to 1.0>, "reasoning": "<one short sentence>"}}
"""
    return prompt

def classify(customer_text, thread=None):
    prompt = build_classification_prompt(customer_text, thread)
    raw_response = call_llm(prompt, model="openai/gpt-oss-120b")
    
    try:
        cleaned = raw_response.replace("```json", "").replace("```", "").strip()
        result = json.loads(cleaned)
        return result
    except json.JSONDecodeError:
        return {"intent": "unknown", "confidence": 0.0, "reasoning": f"Failed to parse: {raw_response}"}

if __name__ == "__main__":
    test_messages = [
        "app keeps crashing every time I try to shuffle my playlist",
        "I was charged but my premium never activated, please help",
        "can't login, password reset link isn't working",
        "thank you so much, it's working now!",
        "please add an alarm clock feature to the app",
    ]
    
    for msg in test_messages:
        result = classify(msg)
        print(f"Message: {msg}")
        print(f"  → Intent: {result['intent']} (confidence: {result.get('confidence', 'N/A')})")
        print(f"  → Reasoning: {result.get('reasoning', 'N/A')}\n")
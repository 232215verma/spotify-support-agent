from llm_client import call_llm
from retrieve import retrieve_similar
import json

def build_reply_prompt(customer_text, similar_cases, intent):
    examples_block = ""
    for i, case in enumerate(similar_cases, 1):
        examples_block += f"""
Example {i} (similarity: {case['similarity']:.2f}):
Customer: {case['customer_text']}
Spotify's reply: {case['brand_reply']}
"""

    prompt = f"""You are a Spotify customer support agent replying on Twitter, in Spotify's tone: friendly, concise, helpful, and casual but professional. Replies are usually under 280 characters.

Here are real past examples of how Spotify support has resolved similar issues (intent: {intent}):
{examples_block}

Now, based on the PATTERN shown in these examples (not copying them word-for-word), draft a reply to this new customer message:

Customer: "{customer_text}"

Respond with ONLY valid JSON in this format:
{{"reply": "<your drafted reply>", "grounded_on": "<one short sentence on which example(s) informed this reply>"}}
"""
    return prompt

def draft_reply(customer_text, intent, top_k=3):
    similar_cases = retrieve_similar(customer_text, top_k=top_k)
    prompt = build_reply_prompt(customer_text, similar_cases, intent)
    raw_response = call_llm(prompt, max_tokens=500, model="openai/gpt-oss-120b")

    try:
        cleaned = raw_response.replace("```json", "").replace("```", "").strip()
        result = json.loads(cleaned)
        result["retrieved_examples"] = similar_cases
        return result
    except json.JSONDecodeError:
        print(f"\n[DEBUG] Raw response that failed to parse:\n{raw_response}\n")
        return {"reply": raw_response, "grounded_on": "parse_error", "retrieved_examples": similar_cases}

if __name__ == "__main__":
    test_query = "app keeps crashing when I try to shuffle my playlist"
    result = draft_reply(test_query, intent="playback_bug")

    print(f"Customer: {test_query}\n")
    print(f"Drafted reply: {result['reply']}")
    print(f"Grounded on: {result['grounded_on']}")
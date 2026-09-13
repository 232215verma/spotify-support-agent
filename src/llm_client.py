from groq import Groq
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt, model="openai/gpt-oss-20b", temperature=0.0, max_tokens=500, retries=3):
    """Single wrapper for all LLM calls — keeps things consistent across the project."""
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            choice = response.choices[0]
            content = choice.message.content
            finish_reason = choice.finish_reason

            if content and content.strip():
                return content.strip()
            else:
                print(f"[WARN] Empty response on attempt {attempt+1}. finish_reason={finish_reason}, retrying...")
                time.sleep(1)
        except Exception as e:
            print(f"[WARN] API error on attempt {attempt+1}: {e}, retrying...")
            time.sleep(1)

    return ""
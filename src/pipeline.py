from data_prep import load_raw, get_thread_context
from classify_intent import classify
from draft_reply import draft_reply
from escalate import decide_escalation
import json

def run_agent(customer_text, thread=None):
    """
    Full pipeline: classify intent -> draft grounded reply -> decide escalation.
    Returns a single structured result.
    """
    # 1. Classify intent (with thread context if available)
    classification = classify(customer_text, thread=thread)
    intent = classification["intent"]
    confidence = classification.get("confidence", 0.0)

    # 2. Decide escalation
    escalation = decide_escalation(intent, confidence)

    # 3. Draft a reply — always draft one, even if escalating,
    #    so a human has a starting point (this is a design choice worth noting in the decision log)
    draft = draft_reply(customer_text, intent=intent)

    return {
        "customer_text": customer_text,
        "intent": intent,
        "confidence": confidence,
        "classification_reasoning": classification.get("reasoning", ""),
        "escalate": escalation["escalate"],
        "escalation_reason": escalation["reason"],
        "drafted_reply": draft["reply"],
        "reply_grounded_on": draft.get("grounded_on", ""),
    }

if __name__ == "__main__":
    test_messages = [
        "app keeps crashing every time I try to shuffle my playlist",
        "I was charged but my premium never activated, please help",
        "thank you so much, it's working now!",
    ]

    for msg in test_messages:
        result = run_agent(msg)
        print("=" * 70)
        print(f"Customer: {result['customer_text']}")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']})")
        print(f"Escalate: {result['escalate']}")
        print(f"Reason: {result['escalation_reason']}")
        print(f"Drafted reply: {result['drafted_reply']}")
        print()
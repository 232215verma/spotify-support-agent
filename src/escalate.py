from intents import ESCALATE_BY_DEFAULT

CONFIDENCE_THRESHOLD = 0.6  # below this, escalate regardless of intent

def decide_escalation(intent, confidence):
    """
    Returns a dict: {"escalate": bool, "reason": str}
    Combines two signals:
    1. Intent-type default (some intents are inherently security/money-sensitive)
    2. Classifier confidence (low confidence = uncertain = needs human review)
    """
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "escalate": True,
            "reason": f"Low classification confidence ({confidence:.2f} < {CONFIDENCE_THRESHOLD}) — model is uncertain about intent, needs human review."
        }

    intent_default = ESCALATE_BY_DEFAULT.get(intent, True)  # unknown intents default to escalate (safe default)
    if intent_default:
        return {
            "escalate": True,
            "reason": f"Intent '{intent}' is security/money-sensitive by default (e.g. requires account-level verification)."
        }

    return {
        "escalate": False,
        "reason": f"Intent '{intent}' with high confidence ({confidence:.2f}) — safe to auto-handle with a templated/grounded reply."
    }

if __name__ == "__main__":
    test_cases = [
        {"intent": "playback_bug", "confidence": 0.9},
        {"intent": "billing_subscription", "confidence": 0.95},
        {"intent": "login_account_access", "confidence": 0.99},
        {"intent": "feature_request", "confidence": 0.3},  # low confidence
        {"intent": "resolved_positive", "confidence": 0.99},
    ]

    for case in test_cases:
        result = decide_escalation(case["intent"], case["confidence"])
        print(f"Intent: {case['intent']}, Confidence: {case['confidence']}")
        print(f"  → Escalate: {result['escalate']}")
        print(f"  → Reason: {result['reason']}\n")
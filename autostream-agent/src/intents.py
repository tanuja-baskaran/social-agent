from enum import Enum

class Intent(Enum):
    GREETING = "greeting"
    PRICING_INQUIRY = "pricing_inquiry"
    HIGH_INTENT_LEAD = "high_intent_lead"
    OTHER = "other"

HIGH_INTENT_KEYWORDS = [
    "sign up", "subscribe", "buy", "purchase", "start pro", "try pro", "activate",
    "ready to", "i want pro", "upgrade", "my youtube", "my instagram"
]

def detect_intent(user_text: str) -> Intent:
    t = user_text.lower().strip()
    if any(word in t for word in ["hi", "hello", "hey"]):
        return Intent.GREETING
    if any(word in t for word in ["price", "pricing", "cost", "plans", "features"]):
        return Intent.PRICING_INQUIRY
    if any(k in t for k in HIGH_INTENT_KEYWORDS):
        return Intent.HIGH_INTENT_LEAD
    return Intent.OTHER

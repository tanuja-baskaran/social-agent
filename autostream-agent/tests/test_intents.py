from src.intents import detect_intent, Intent

def test_greeting():
    assert detect_intent("Hey there") == Intent.GREETING

def test_pricing():
    assert detect_intent("What are your plans and pricing?") == Intent.PRICING_INQUIRY

def test_high_intent():
    assert detect_intent("I want to sign up for Pro for my YouTube") == Intent.HIGH_INTENT_LEAD

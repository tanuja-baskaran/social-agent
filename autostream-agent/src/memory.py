from dataclasses import dataclass, field

@dataclass
class ConversationState:
    history: list = field(default_factory=list)
    lead: dict = field(default_factory=lambda: {"name": None, "email": None, "platform": None})
    pending_lead_fields: list = field(default_factory=list)
    last_intent: str = None
    previous_intent: str = None # Added to track state transitions

    def remember(self, role: str, text: str):
        self.history.append({"role": role, "text": text})
        # Trim to last ~6 turns to meet the requirement
        self.history = self.history[-12:]

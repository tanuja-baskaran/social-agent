import json
from pathlib import Path

class KnowledgeBase:
    def __init__(self, json_path="data/kb.json"):
        import os
        # Fallback to absolute path content if relative fails, or just standard load
        try:
            self.data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        except FileNotFoundError:
             # Try finding it relative to the package if running as module
             base_dir = Path(__file__).parent.parent
             self.data = json.loads((base_dir / "data/kb.json").read_text(encoding="utf-8"))

    def get_content_as_text(self):
        """Returns the entire KB as a text string for the LLM context."""
        plans = self.data.get("plans", {})
        policies = self.data.get("policies", {})
        
        text = "## Pricing Plans\n"
        for name, details in plans.items():
            text += f"- Plan: {name}\n"
            text += f"  - Price: ${details['price_per_month']}/month\n"
            text += f"  - Video Limit: {details['video_limit_per_month']}\n"
            text += f"  - Resolution: {details['max_resolution']}\n"
            if details['features']:
                text += f"  - Features: {', '.join(details['features'])}\n"
        
        text += "\n## Policies\n"
        text += f"- Refunds: {policies.get('refunds')}\n"
        text += f"- Support: {policies.get('support')}\n"
        
        return text

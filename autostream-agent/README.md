# AutoStream Social-to-Lead Agent

A LangGraph-based conversational agent with RAG over a local KB, intent detection, and guarded tool execution for lead capture.

## How to run locally
1. Create a virtual environment and install dependencies:
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
2. Ensure data/kb.json exists (provided).
3. Run the CLI:
   - python -m src.main

## Architecture explanation (~200 words)
- Choice of LangGraph:
  LangGraph provides explicit state graphs, letting us wire nodes for classification, answering (RAG), and lead collection while preserving conversation state. Its compile-time graph model makes tool-calling and routing transparent and testable.
- RAG:
  The agent queries a local JSON (with optional MD fallback) to deterministically serve pricing, features, and policies. This guarantees accuracy and avoids hallucinations.
- State management:
  A dataclass-based ConversationState tracks short-term memory (last ~6 turns), current intent, and a lead object with required fields (name, email, platform). The graph routes the user through a strict sequence: detect intent → answer via RAG → collect missing lead fields → execute mock tool only when all fields are present. This enforces proper tool calling and prevents premature execution.

## WhatsApp integration (webhooks)
- Use WhatsApp Cloud API (Meta) or Twilio WhatsApp:
  1. Expose a webhook endpoint (e.g., Flask/FastAPI) to receive messages.
  2. Map incoming WhatsApp messages to the agent’s `classify → answer → collect` flow, persisting ConversationState per user (keyed by phone number) in Redis.
  3. Send agent responses back via the provider’s send-message API.
  4. Secure with verification tokens and signature validation; handle retries idempotently.
  5. For deployment, host on a public URL (e.g., Render/Cloud Run) and register webhook in the provider’s console.

## Demo instructions
Record a screen session:
1. Ask “Hi, tell me about your pricing.”
2. Agent replies with Basic/Pro pricing and policies (from KB).
3. Say “I want to try the Pro plan for my YouTube channel.”
4. Agent detects high intent and starts collecting name → email → platform.
5. Provide all details; observe “Lead captured successfully...” message.

## Tests
- `tests/test_intents.py` covers intent detection heuristics.

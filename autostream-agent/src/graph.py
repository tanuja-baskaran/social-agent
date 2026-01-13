from langgraph.graph import StateGraph, END
from src.memory import ConversationState
from src.intents import detect_intent, Intent
from src.rag import KnowledgeBase
from src.tools import mock_lead_capture
from src.llm import generate_rag_response

# Initialize KB
kb = KnowledgeBase()
kb_context = kb.get_content_as_text()

def node_classify(state: ConversationState, user_text: str = ""):
    # Save previous intent to detect transitions
    state.previous_intent = state.last_intent
    
    intent_enum = detect_intent(user_text)
    state.last_intent = intent_enum.value
    state.remember("user", user_text)
    return state

def node_answer(state: ConversationState):
    intent = Intent(state.last_intent)
    
    # Logic:
    # If GREETING -> Simple static reply or LLM
    # If PRICING/OTHER -> RAG via LLM
    # If HIGH_INTENT -> Lead collection flow (deterministic)
    
    if intent == Intent.HIGH_INTENT_LEAD:
        # Check missing fields
        missing = [k for k, v in state.lead.items() if not v]
        state.pending_lead_fields = missing
        
        if missing:
            first = missing[0]
            prompts = {
                "name": "That sounds great! To get you started on Pro, what is your full name?",
                "email": "Thanks! Could you please share your email address?",
                "platform": "Which creator platform do you use (e.g., YouTube, Instagram)?"
            }
            reply = prompts.get(first, "Could you provide that detail?")
        else:
            reply = "I have all your details. Let me sign you up."
            
    elif intent == Intent.GREETING:
         # We can use LLM here too for personality, but static is faster.
         reply = "Hi there! I'm the AutoStream assistant. I can help you with our pricing plans or getting signed up. What would you like to know?"
         
    else:
        # PRICING_INQUIRY or OTHER
        # Use LLM + RAG for natural language answers based on JSON data
        try:
            reply = generate_rag_response(state.history, kb_context)
        except Exception as e:
            # Fallback if OpenAI key is missing or error
            # print(f"LLM Error: {e}") 
            reply = "I can tell you about our Basic ($29) and Pro ($79) plans. Which one are you interested in?"

    state.remember("assistant", reply)
    return state

def node_collect(state: ConversationState, user_text: str = ""):
    # FIX: Check if this is the start of the flow (Trigger phrase)
    # If we just switched to HIGH_INTENT from something else (or None), this text was the trigger ("I want pro").
    # We should NOT assume it is the Name/Email/Platform unless we extracted it (which we aren't doing here).
    
    if state.last_intent == Intent.HIGH_INTENT_LEAD.value and state.previous_intent != Intent.HIGH_INTENT_LEAD.value:
        # This turns triggers the flow. The USER text is "I want pro". 
        # The AGENT reply (from node_answer) is "What is your name?".
        # We should NOT collect "I want pro" as the name.
        return state, None

    # Lead collection logic remains deterministic to ensure data integrity
    if state.pending_lead_fields:
        field = state.pending_lead_fields[0]
        state.lead[field] = user_text.strip()
        state.pending_lead_fields = [f for f in state.pending_lead_fields if f != field]

    if all(state.lead.values()):
        result = mock_lead_capture(**state.lead)
        reply = f"Perfect! I've captured your details ({result['name']}). A member of our team will contact you at {result['email']} shortly to set up your account."
        state.remember("assistant", reply)
        return state, reply

    if state.pending_lead_fields:
        next_field = state.pending_lead_fields[0]
        prompts = {
            "name": "What is your full name?",
            "email": "What is your email address?",
            "platform": "Which platform do you use?"
        }
        reply = prompts.get(next_field, "Please provide the next detail.")
        state.remember("assistant", reply)
        return state, reply

    return state, None

def build_graph():
    g = StateGraph(ConversationState)
    
    g.add_node("classify", node_classify)
    g.add_node("answer", node_answer)
    g.add_node("collect", node_collect)

    g.set_entry_point("classify")
    g.add_edge("classify", "answer")
    g.add_edge("answer", "collect")
    g.add_edge("collect", END)

    return g.compile()

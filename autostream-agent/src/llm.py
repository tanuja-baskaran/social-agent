from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def get_llm():
    """But initialize the LLM (GPT-4o-mini)."""
    # Requires OPENAI_API_KEY in environment variables
    # We use temperature=0 for more deterministic behavior
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_rag_response(history: list, context: str):
    llm = get_llm()
    
    # Construct message history
    messages = [
        SystemMessage(content=f"""You are the friendly AI assistant for AutoStream, a video creation platform.
Use the following context to answer user questions. 
If the answer is not in the context, politely say you don't know.
Keep answers concise and helpful.

CONTEXT:
{context}
""")
    ]
    
    # Add conversation history (last 5-6 turns)
    for msg in history:
        if msg['role'] == 'user':
            messages.append(HumanMessage(content=msg['text']))
        elif msg['role'] == 'assistant':
            messages.append(AIMessage(content=msg['text']))
            
    # Generate response
    response = llm.invoke(messages)
    return response.content

def classify_intent_with_llm(user_text: str):
    """Optional: Use LLM for stricter intent classification if heuristics fail."""
    llm = get_llm()
    messages = [
        SystemMessage(content="""Classify the user's intent into exactly one of these categories:
- GREETING (hi, hello, etc)
- PRICING_INQUIRY (asking about cost, plans, features)
- HIGH_INTENT_LEAD (wanting to buy, sign up, upgrade, providing specific channel info)
- OTHER

Return JUST the category name.
"""),
        HumanMessage(content=user_text)
    ]
    response = llm.invoke(messages)
    return response.content.strip().upper()

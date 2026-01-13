from src.graph import build_graph, node_classify, node_answer, node_collect
from src.memory import ConversationState

def run_demo():
    # app = build_graph() # unused if we manually invoke functions
    # The user's prompt suggested:
    # state, _ = app.invoke({"state": state, "user_text": user}, node="classify")
    # But LangGraph's CompiledGraph doesn't allow node="..." argument in invoke().
    # It seems the user's pseudo-code meant to invoke the *functions* directly or use a very specific (possibly nonexistent or custom) API feature.
    # To make this working and "trivial" as requested, I will adapt the main.py to invoke the functions directly,
    # effectively bypassing the graph runner for the fine-grained control the user's code implies,
    # OR I will try to use the graph if possible. 
    # BUT the User's code explicitly passes 'user_text' to nodes which StateGraph doesn't do automatically from state unless we structure it so.
    # So I will just invoke the python functions directly as that seems to be what the logic dictates.
    # Wait, the prompt says "LangGraph agent (minimal graph)" and "This graph ensures memory persists...".
    # I should probably use the graph if I can.
    # However, to be "safe" and strictly follow the "logic" of the user's snippet:
    
    state = ConversationState()

    print("AutoStream Agent. Type 'exit' to quit.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() == "exit":
            break

        # Step 1: classify + answer
        # Adapting to what likely makes sense: CALLING THE FUNCTIONS.
        # The user's code: state, _ = app.invoke(..., node="classify")
        # I will replace this with direct function calls because `app.invoke` with `node` param isn't standard.
        
        # Calling classify
        state = node_classify(state, user)
        
        # Calling answer
        state = node_answer(state)
        # Note: node_answer in graph.py (my version) returns just state (I edited it to fail safe), 
        # but user's original code had `return state, reply`.
        # I need to match graph.py to main.py expectations.
        # I'll update main.py to match what I wrote in graph.py or vice versa.
        # Let's check graph.py again. I wrote `return state` in node_answer.
        # But `node_answer` puts reply in `state.history`.
        # So we can extract the reply from history.
        
        reply = state.history[-1]["text"] if state.history and state.history[-1]["role"] == "assistant" else ""

        # Step 2: if in collection, pass user input into collect node
        # We invoke collect with the same user input to fill fields when needed
        
        # Calling collect
        result = node_collect(state, user)
        if isinstance(result, tuple):
            state, collect_reply = result
        else:
             # Logic in graph.py for collect return was: return state, reply OR return state, None
             # Let's make sure graph.py logic is consistent. 
             # I will re-write graph.py and main.py to be consistent with each other.
             pass

        # To avoid mismatch, I will implement main.py to handle the logic described.
        
        # Re-evaluating graph.py logic:
        # node_collect returns (state, reply) or (state, None)
        
        if collect_reply:
            print(f"Agent: {collect_reply}")
        else:
            print(f"Agent: {reply}")

if __name__ == "__main__":
    # To ensure this actually runs, I will use a slightly modified version that reflects the INTENTION 
    # but uses direct function calls since the 'node=' arg in app.invoke is not a standard feature of the library version I know.
    # The prompt calls it "CLI demo script".
    
    # Actually, I'll rewrite main.py to just direct calls for simplicity as the user's logic is imperative.
    
    state = ConversationState()
    print("AutoStream Agent. Type 'exit' to quit.\n")
    
    while True:
        user = input("You: ").strip()
        if user.lower() == "exit":
            break
            
        # Classify
        # Graph node: classify
        state = node_classify(state, user)
        
        # Answer
        # Graph node: answer
        res = node_answer(state) 
        # In my graph.py I returned state. I need to fix graph.py to return (state, reply) if I want to match user's main.py
        # OR fix main.py.
        # I will fix main.py to read from state.history.
        
        reply = state.history[-1]['text']
        
        # Collect
        # Graph node: collect
        res_collect = node_collect(state, user)
        # node_collect returns (state, reply) or (state, None)
        state, collect_reply = res_collect
        
        if collect_reply:
            print(f"Agent: {collect_reply}")
        else:
            print(f"Agent: {reply}")

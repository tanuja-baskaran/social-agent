from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.memory import ConversationState
from src.graph import node_classify, node_answer, node_collect
import uuid
import uvicorn

app = FastAPI(title="AutoStream Agent API")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = ""

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = ConversationState()
    
    state = sessions[session_id]
    user_text = request.message
    
    # 1. Classify
    # Updates state with intent and user memory
    state = node_classify(state, user_text)
    
    # 2. Answer
    # Updates state with RAG-based answer based on intent
    state = node_answer(state)
    
    # Extract the RAG answer
    rag_reply = ""
    if state.history and state.history[-1]["role"] == "assistant":
        rag_reply = state.history[-1]["text"]

    # 3. Collect
    # Needs the user input again to fill slots if we are in HIGH_INTENT/collection mode
    result = node_collect(state, user_text)
    
    collect_reply = None
    if isinstance(result, tuple):
        state, collect_reply = result
    
    # Logic: The agent always produces a RAG reply in 'node_answer'. 
    # 'node_collect' might produce a DIFFERENT reply (asking for slots or confirming lead).
    # If 'node_collect' has something to say, it takes precedence (overwrites or follows).
    # In this simple flow, we return the collect_reply if it exists, otherwise the rag_reply.
    
    final_reply = collect_reply if collect_reply else rag_reply
    
    return ChatResponse(response=final_reply, session_id=session_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

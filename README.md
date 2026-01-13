# AutoStream Social-to-Lead Agent

A production-ready conversational AI designed to automate lead qualification on social platforms. Built using the **LangGraph** framework for strict state management and **FastAPI** for deployment.

## Key Features
*   **🧠 Intelligent Orchestration**: Uses a state graph to manage conversation flow between greeting, RAG-based Q&A, and structured data collection.
*   **📚 RAG Pipeline**: Deterministically answers pricing and policy questions using a local Knowledge Base (JSON/Markdown) to prevent hallucinations.
*   **🎯 Intent Detection**: Hybrid classification (Heuristic + LLM) to identify high-intent leads instantly.
*   **💾 Context Awareness**: Retains short-term memory across 5-6 conversation turns for natural interactions.
*   **✨ Premium UI**: Includes a responsive, dark-mode web interface for demonstration and testing.

## Technology Stack
*   **Language**: Python 3.13
*   **Frameworks**: LangGraph, LangChain, FastAPI
*   **AI Models**: OpenAI GPT-4o-mini
*   **Frontend**: HTML5, Vanilla CSS (Premium Dark Mode), JavaScript

## Project Structure
The core agent code is located in the `autostream-agent/` directory:

```
autostream-agent/
├── data/           # Knowledge Base (JSON/MD)
├── src/            # Source Code
│   ├── api.py      # FastAPI Backend
│   ├── graph.py    # LangGraph State Machine
│   ├── rag.py      # RAG Logic
│   └── ...
├── web/            # Frontend Web Interface
└── requirements.txt
```

## Getting Started

To run the agent locally:

1.  Navigate to the agent directory:
    ```bash
    cd autostream-agent
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set your OpenAI API Key:
    ```bash
    # Windows PowerShell
    $env:OPENAI_API_KEY="your-key-here"
    ```
4.  Run the API server:
    ```bash
    python -m src.api
    ```
5.  Open `web/index.html` in your browser.

For more detailed technical documentation, please refer to [autostream-agent/README.md](autostream-agent/README.md).

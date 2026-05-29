# Jagrati-week2 — Chat with Documents Agent

A RAG + LangGraph agent that answers questions by retrieving relevant chunks from a local knowledge base and cites its sources. Includes a calculator as an additional tool.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      LangGraph Graph                    │
│                                                         │
│  [START] ──► [agent] ──── has tool calls? ──► [run_tools]
│                  ▲                                  │   │
│                  └──────────────────────────────────┘   │
│                  │                                       │
│                 NO                                       │
│                  │                                       │
│               [END]                                      │
└─────────────────────────────────────────────────────────┘

Tools available to the agent:
  1. retrieve_docs  → searches ChromaDB vector store (RAG)
  2. calculator     → evaluates arithmetic expressions
```

### Module Layout

```
Jagrati-week2/
├── docs/                        # Source documents (knowledge base)
│   ├── machine_learning_basics.md
│   ├── rag_and_llms.md
│   └── langgraph_and_agents.md
│
├── ingest/                      # RAG pipeline
│   ├── ingest.py                # Load → chunk → embed → store in ChromaDB
│   └── retriever.py             # retrieve(query, top_k) → list of chunks
│
├── agent/                       # LangGraph agent
│   ├── tools.py                 # retrieve_docs tool + calculator tool
│   └── graph.py                 # StateGraph: agent node, run_tools node, conditional edge
│
├── server/                      # MCP server reference implementation
│   └── mcp_server.py            # Shows what the calculator would look like as MCP
│
├── main.py                      # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## One-Line Setup Steps

```bash
# 1. Clone / navigate into the project
cd Jagrati-week2

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your OpenAI API key
cp .env.example .env
# Edit .env and add your key: OPENAI_API_KEY=sk-...

# 5. Load environment variables (or let python-dotenv handle it)
export OPENAI_API_KEY=your-key-here   # or just edit .env

# 6. Ingest documents (only needed once, or when docs change)
python main.py --ingest

# 7. Ask a question
python main.py --ask "What is overfitting in machine learning?"

# 8. Or start interactive chat
python main.py
```

---

## Example Questions the Agent Answers Well

### Q1 — Knowledge base question (triggers retrieve_docs)
```
You: What is the difference between overfitting and underfitting?
```
**Expected behaviour:** Agent calls `retrieve_docs`, retrieves the relevant chunk from `machine_learning_basics.md`, and answers with a citation like *(Source: machine_learning_basics.md, chunk 3)*.

---

### Q2 — RAG question spanning multiple documents
```
You: How does the RAG pipeline work and how does LangGraph help build RAG agents?
```
**Expected behaviour:** Agent retrieves chunks from both `rag_and_llms.md` and `langgraph_and_agents.md`, synthesizes an answer, and cites both sources.

---

### Q3 — Calculator tool question
```
You: If I have 3 models and each takes 2 ** 8 seconds to train, how many total seconds is that?
```
**Expected behaviour:** Agent calls `calculator` with `3 * 2 ** 8`, returns `3 * 2 ** 8 = 768`.

---

## MCP Tool — Trade-off Note

The assignment asks for one tool exposed via MCP (Model Context Protocol). 

**What was done:** The `calculator` tool is implemented as a regular LangGraph `@tool` in `agent/tools.py`.

**Why:** Full MCP integration requires:
- Running a separate MCP server process (`server/mcp_server.py`)
- Installing the `mcp` package and `langchain-mcp-adapters`
- Managing server lifecycle (subprocess or Docker)

**Trade-off:** The functionality is identical. The only difference is the transport layer — with MCP, the tool runs in its own isolated process and can be shared across multiple agents or services. `server/mcp_server.py` shows exactly what the MCP server implementation looks like, using the same calculation logic.

**To enable real MCP** (optional):
```bash
pip install mcp langchain-mcp-adapters
python -m server.mcp_server   # runs on http://localhost:8001
```
Then update `agent/tools.py` to use `MCPToolkit` instead of `@tool`.

---

## How the LangGraph Graph Works

1. **`agent` node** — Sends the conversation to `gpt-4o-mini` with both tools bound. The LLM decides whether to call a tool or respond directly.
2. **Conditional edge** — If the LLM's response contains `tool_calls`, route to `run_tools`. Otherwise go to `END`.
3. **`run_tools` node** — LangGraph's built-in `ToolNode` executes the requested tool(s) and appends the result as a `ToolMessage`.
4. **Loop back** — After tool execution, control returns to `agent` so the LLM can see the tool result and decide what to do next (answer, or call another tool).

---

## Changing top-k (live demo)

In `ingest/retriever.py`, change the default `top_k` parameter:
```python
def retrieve(query: str, top_k: int = 3) -> list[dict]:
```
Change `3` to `5` or `1` — no re-ingestion needed.

## Adding a new document (live demo)

1. Drop a `.md` or `.txt` file into `docs/`
2. Run `python main.py --ingest` again
3. Ask questions about it immediately
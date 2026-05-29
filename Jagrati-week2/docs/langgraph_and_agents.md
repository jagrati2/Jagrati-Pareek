# LangGraph and AI Agents

## What is LangGraph?
LangGraph is a library built on top of LangChain for building stateful, multi-actor applications with LLMs. It models agent workflows as directed graphs where nodes represent computation steps and edges represent transitions between steps.

## Core Concepts

### Nodes
Nodes are Python functions or Runnables that perform a unit of work. Each node receives the current state, performs some computation, and returns an update to the state. Examples:
- An agent node that calls an LLM
- A tool node that executes a tool
- A retrieval node that fetches documents

### Edges
Edges define how control flows between nodes. Types of edges:
- Normal edges: Always go from node A to node B
- Conditional edges: Go to different nodes based on some condition (e.g., did the agent decide to retrieve?)
- Entry point: Specifies the starting node
- End point: Specifies where the graph terminates (END node)

### State
LangGraph maintains a shared state object that is passed between nodes. The state is typically a TypedDict or Pydantic model. Each node reads from and writes to this state.

### StateGraph
The main class used to define the graph. You add nodes and edges to it, then compile it into a runnable.

## Why LangGraph over Simple Chains?

### Cycles and Loops
Unlike simple chains (which are DAGs), LangGraph supports cycles. This allows agents to loop: retrieve → think → retrieve again if needed.

### Human-in-the-Loop
LangGraph supports pausing execution to wait for human input, making it suitable for approval workflows.

### Persistence
LangGraph can persist state across conversations using checkpointers (SQLite, PostgreSQL), enabling multi-turn conversations with memory.

### Multi-Agent Systems
LangGraph supports multiple agents communicating with each other, each with their own state and tools.

## Building a Simple Agent Graph

### Step 1: Define State
```python
from typing import TypedDict, List
class AgentState(TypedDict):
    messages: List
    retrieved_docs: List
```

### Step 2: Define Nodes
Each node is a function that takes state and returns state updates.

### Step 3: Add Conditional Logic
Use `add_conditional_edges` to let the agent decide: should it retrieve documents or answer directly?

### Step 4: Compile and Run
```python
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("retrieve", retrieve_node)
app = graph.compile()
result = app.invoke({"messages": [HumanMessage(content="What is RAG?")]})
```

## ReAct Pattern
LangGraph commonly implements the ReAct (Reasoning + Acting) pattern:
1. Reason: The agent thinks about what to do
2. Act: The agent takes an action (calls a tool or retrieves)
3. Observe: The agent observes the result
4. Repeat until a final answer is reached

## Tool Calling
Agents can call tools (functions) to gather information or perform actions. Tools are bound to the LLM and the model decides when to call them. LangGraph's ToolNode automatically handles tool execution and returns results back to the agent.

## Checkpointing and Memory
LangGraph supports short-term memory (within a conversation via state) and long-term memory (across conversations via external storage). The MemorySaver checkpointer stores state in-memory for development.
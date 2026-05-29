"""
agent/graph.py

Defines the LangGraph agent graph:

  [START]
     │
  [agent]  ──── needs_tool? ──── YES ──► [run_tools]
     ▲                                       │
     └───────────────────────────────────────┘
     │
    NO
     │
  [END]

Nodes:
  - agent     : calls the LLM (with tools bound); decides to retrieve or answer
  - run_tools : executes whichever tool(s) the LLM chose (retrieve_docs / calculator)

Conditional edge:
  After `agent`, if the LLM emitted tool_calls → go to `run_tools`
  Otherwise → go to END
"""

from typing import Annotated
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()  # loads OPENAI_API_KEY from .env file

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from agent.tools import TOOLS

# ── State ─────────────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    # add_messages merges new messages into the list instead of replacing it
    messages: Annotated[list[BaseMessage], add_messages]


# ── LLM ───────────────────────────────────────────────────────────────────────

def get_llm():
    """Return an LLM with tools bound."""
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    return llm.bind_tools(TOOLS)

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful assistant with access to two tools:

1. retrieve_docs - searches a knowledge base about machine learning, RAG, and LangGraph.
   Call this tool ONLY. Do not write any answer text in the same response as a tool call.

2. calculator - evaluates arithmetic expressions.
   Call this tool ONLY. Do not write any answer text in the same response as a tool call.

After the tool result comes back, write your full answer using that information.
End your answer with: Sources: [filename, chunk N]

For greetings or general questions, reply directly without calling any tool.
"""


# ── Nodes ─────────────────────────────────────────────────────────────────────

def agent_node(state: AgentState) -> dict:
    """LLM decides whether to call a tool or answer directly."""
    llm = get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """Conditional edge: route to tools if the LLM made tool calls, else END."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "run_tools"
    return END


# ── Build graph ───────────────────────────────────────────────────────────────

def build_graph():
    tool_node = ToolNode(TOOLS)

    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("run_tools", tool_node)

    # Entry point
    graph.set_entry_point("agent")

    # Conditional edge after agent
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "run_tools": "run_tools",
            END: END,
        },
    )

    # After tools execute, always go back to agent
    graph.add_edge("run_tools", "agent")

    return graph.compile()


# ── Convenience runner ────────────────────────────────────────────────────────

def run_agent(question: str) -> str:
    """Run the agent with a single user question and return the final answer."""
    from langchain_core.messages import HumanMessage

    app = build_graph()
    result = app.invoke({"messages": [HumanMessage(content=question)]})

    # The last message is the final LLM response
    final_message = result["messages"][-1]
    return final_message.content
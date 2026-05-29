"""
agent/tools.py

Defines the tools available to the agent:
  1. retrieve_docs  – RAG retrieval from ChromaDB
  2. calculator     – simple arithmetic evaluator (the MCP-style additional tool)

NOTE on MCP trade-off:
  The assignment asks for one tool via MCP (Model Context Protocol).
  Full MCP requires running a separate MCP server process and wiring the
  LangGraph agent to it via an MCP client.  To keep setup simple and focus
  on demonstrating the concept clearly, `calculator` is exposed here as a
  regular LangGraph tool (using @tool).  The trade-off is that with a real
  MCP server the tool would live in its own isolated process and could be
  shared across multiple agents or services — here it is co-located with
  the agent.  The /server/ folder shows what the MCP server would look like.
"""

import ast
import operator

from langchain_core.tools import tool

from ingest.retriever import retrieve


# ── Tool 1: Document Retrieval ────────────────────────────────────────────────

@tool
def retrieve_docs(query: str) -> str:
    """
    Search the knowledge base for information relevant to the query.
    Use this tool when the question is about machine learning, RAG,
    LangGraph, AI agents, or any topic that might be in the documents.
    Returns the top matching chunks with source citations.
    """
    chunks = retrieve(query, top_k=3)
    if not chunks:
        return "No relevant documents found."

    parts = []
    for chunk in chunks:
        citation = f"[Source: {chunk['source']}, chunk {chunk['chunk_index']}]"
        parts.append(f"{citation}\nContent: {chunk['content']}")
    
    return (
        "Here are the relevant excerpts from the knowledge base:\n\n"
        + "\n\n---\n\n".join(parts)
        + "\n\nUse the above content to write a full answer. Always include the source citations at the end."
    )


# ── Tool 2: Calculator ────────────────────────────────────────────────────────

# Safe operators only
_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    """Recursively evaluate an AST node using only safe operators."""
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op_type}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _SAFE_OPS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op_type}")
        return _SAFE_OPS[op_type](_safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported expression type: {type(node)}")


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a simple arithmetic expression and return the result.
    Supports: +, -, *, /, ** (power).
    Examples: '2 + 3', '10 / 4', '2 ** 8', '(3 + 5) * 2'
    Use this tool when the user asks to calculate or compute something.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree.body)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


# ── Export ────────────────────────────────────────────────────────────────────
TOOLS = [retrieve_docs, calculator]
"""
server/mcp_server.py

This is what the calculator tool would look like as a proper MCP
(Model Context Protocol) server.

MCP servers run as independent processes and expose tools over
a standard JSON-RPC protocol. An MCP client (e.g. LangChain's
MCPToolkit) would connect to this server, discover its tools,
and make them available to any LangGraph agent.

Trade-off in this project:
  Full MCP integration requires:
    1. Running this server as a subprocess or separate service
    2. Using MCPToolkit / langchain-mcp-adapters to wrap the tools
    3. Managing the lifecycle of the server process

  For clarity and ease of setup (no extra process management),
  the calculator is exposed as a regular LangGraph @tool in
  agent/tools.py.  The logic is identical — only the transport
  layer differs.

How to run this server standalone (for reference):
  pip install mcp
  python -m server.mcp_server

The agent would then connect with:
  from langchain_mcp_adapters.client import MultiServerMCPClient
  client = MultiServerMCPClient({"calculator": {"url": "http://localhost:8001/mcp"}})
  tools = await client.get_tools()
"""

import ast
import operator

# ── Safe arithmetic evaluator (same logic as agent/tools.py) ─────────────────

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op_type}")
        return _SAFE_OPS[op_type](_safe_eval(node.left), _safe_eval(node.right))
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _SAFE_OPS:
            raise ValueError(f"Unsupported operator: {op_type}")
        return _SAFE_OPS[op_type](_safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported type: {type(node)}")


def calculate(expression: str) -> str:
    """Core calculation logic shared between MCP and LangGraph tool."""
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        result = _safe_eval(tree.body)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"


# ── MCP Server definition ─────────────────────────────────────────────────────

try:
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("calculator-server")

    @mcp.tool()
    def calculator(expression: str) -> str:
        """
        Evaluate a simple arithmetic expression.
        Supports +, -, *, /, ** (power).
        Examples: '2 + 3', '10 / 4', '2 ** 8'
        """
        return calculate(expression)

    if __name__ == "__main__":
        print("[MCP Server] Starting calculator MCP server on http://localhost:8001")
        mcp.run(transport="streamable-http", host="localhost", port=8001)

except ImportError:
    # mcp package not installed — show a clear message
    if __name__ == "__main__":
        print(
            "[MCP Server] 'mcp' package not installed.\n"
            "Install it with: pip install mcp\n"
            "The calculator is available as a regular LangGraph tool in agent/tools.py"
        )
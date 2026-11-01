from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from app.agent.llm_factory import get_llm
from app.agent.state import SupportState
from app.agent.tools.account_tools import get_user_profile
from app.agent.tools.billing_tools import get_last_order, request_refund_confirmation
from app.agent.tools.knowledge_search import search_knowledge

SYSTEM_PROMPT = """You are CloudNotes' customer-support agent.

Rules:
1. Be concise and helpful.
2. Use tools when needed for account, order, billing, or policy questions.
3. Never invent account, order, refund, or policy details.
4. If information is unavailable, say you cannot find it.
5. For refund requests, first retrieve the order, then ask for confirmation.
6. Never access or discuss another customer's account.
7. If the request is unsafe, ambiguous, or outside your permissions, escalate or ask for clarification.

The authenticated customer's user_id is: {user_id}
Use this user_id when calling account or order tools. Do not ask the user for their user_id.
"""

tools = [
    get_user_profile,
    get_last_order,
    request_refund_confirmation,
    search_knowledge,
]

llm = get_llm()
llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)


def call_model(state: SupportState):
    user_id = state.get("user_id") or "unknown"

    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT.format(user_id=user_id),
    }

    response = llm_with_tools.invoke(
        [system_message] + state["messages"]
    )

    return {"messages": [response]}


def should_continue(state: SupportState):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


builder = StateGraph(SupportState)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
    ["tools", END],
)
builder.add_edge("tools", "agent")

support_graph = builder.compile()
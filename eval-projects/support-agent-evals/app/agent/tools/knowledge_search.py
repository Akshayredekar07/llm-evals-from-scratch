from langchain_core.tools import tool


@tool
def search_knowledge(query: str) -> str:
    """Search the product knowledge base for policies, FAQs, and troubleshooting information."""
    knowledge = {
        "refund": (
            "CloudNotes offers refunds within 14 days for annual plans "
            "if the customer has not used more than 20% of the plan."
        ),
        "order": (
            "Customers can check order status in Billing > Order History. "
            "Orders usually ship within 1 business day."
        ),
        "password": (
            "To reset your password, go to Settings > Security > Reset Password."
        ),
    }

    query_lower = query.lower()

    for keyword, answer in knowledge.items():
        if keyword in query_lower:
            return answer

    return "No relevant knowledge-base article found."
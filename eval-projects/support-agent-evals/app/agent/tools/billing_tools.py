from langchain_core.tools import tool


@tool
def get_last_order(user_id: str) -> str:
    """Get the customer's most recent order, including order ID, status, and amount."""
    fake_orders = {
        "user_123": {
            "order_id": "ORD-1001",
            "status": "shipped",
            "amount": 49.99,
            "item": "CloudNotes Pro annual plan",
        },
        "user_456": {
            "order_id": "ORD-2002",
            "status": "delivered",
            "amount": 9.99,
            "item": "CloudNotes monthly plan",
        },
    }

    order = fake_orders.get(user_id)

    if not order:
        return f"No orders found for user_id={user_id}."

    return str(order)


@tool
def request_refund_confirmation(order_id: str, reason: str) -> str:
    """Ask the customer to confirm a refund request before submitting it."""
    return (
        f"Please confirm: do you want to submit a refund request for order "
        f"{order_id} because: {reason}? Reply yes or no."
    )
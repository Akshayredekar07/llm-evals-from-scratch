from langchain_core.tools import tool


@tool
def get_user_profile(user_id: str) -> str:
    """Get the customer's profile, plan, and account status using their user ID."""
    fake_users = {
        "user_123": {
            "name": "Alex Kumar",
            "email": "alex@example.com",
            "plan": "Pro",
            "status": "active",
        },
        "user_456": {
            "name": "Priya Sharma",
            "email": "priya@example.com",
            "plan": "Free",
            "status": "active",
        },
    }

    user = fake_users.get(user_id)

    if not user:
        return f"No account found for user_id={user_id}."

    return str(user)
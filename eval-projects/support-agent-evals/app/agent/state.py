from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class SupportState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str | None
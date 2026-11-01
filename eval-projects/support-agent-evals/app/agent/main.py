# from dotenv import load_dotenv

# load_dotenv()

# from app.agent.tracing import get_langfuse_handler, phoenix_tracer_provider

# from app.agent.graphs.support_graph import support_graph


# def run_agent(user_message: str, user_id: str | None = None):
#     callbacks = []

#     langfuse_handler = get_langfuse_handler()

#     if langfuse_handler:
#         callbacks.append(langfuse_handler)

#     result = support_graph.invoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": user_message,
#                 }
#             ],
#             "user_id": user_id,
#         },
#         config={
#             "callbacks": callbacks,
#             "metadata": {
#                 "user_id": user_id,
#                 "model_provider": "nebius",
#                 "environment": "local",
#             },
#         },
#     )

#     return {
#         "final_answer": result["messages"][-1].content,
#         "messages": result["messages"],
#     }


# if __name__ == "__main__":
#     output = run_agent(
#         user_message="Where is my order?",
#         user_id="user_123",
#     )

#     print(output["final_answer"])


from dotenv import load_dotenv

load_dotenv()

from app.agent.tracing import tracer_provider  # must come before LangGraph import

from app.agent.graphs.support_graph import support_graph


def run_agent(user_message: str, user_id: str | None = None):
    result = support_graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            "user_id": user_id,
        }
    )

    return {
        "final_answer": result["messages"][-1].content,
        "messages": result["messages"],
    }


if __name__ == "__main__":
    output = run_agent(
        user_message="Where is my order?",
        user_id="user_123",
    )

    print(output["final_answer"])
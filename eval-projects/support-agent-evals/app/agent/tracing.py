# # import os

# # from dotenv import load_dotenv
# # from langfuse.langchain import CallbackHandler

# # load_dotenv()


# # def get_langfuse_handler():
# #     return CallbackHandler()


# # from openinference.instrumentation.langchain import LangChainInstrumentor
# # from phoenix.otel import register

# # tracer_provider = register(
# #     project_name=os.getenv("PHOENIX_PROJECT", "support-agent-dev"),
# #     auto_instrument=True
# # )

# # LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


# import os

# from dotenv import load_dotenv

# load_dotenv()

# from langfuse.langchain import CallbackHandler
# from openinference.instrumentation.langchain import LangChainInstrumentor
# from phoenix.otel import register


# def setup_phoenix():
#     if not os.getenv("PHOENIX_COLLECTOR_ENDPOINT"):
#         return None

#     tracer_provider = register(
#         project_name=os.getenv("PHOENIX_PROJECT", "support-agent-dev"),
#         endpoint=os.getenv(
#             "PHOENIX_COLLECTOR_ENDPOINT",
#             "http://localhost:6006/v1/traces",
#         ),
#         protocol="http/protobuf",
#         auto_instrument=True,
#         set_global_tracer_provider=False,
#     )

#     return tracer_provider


# def get_langfuse_handler():
#     if not os.getenv("LANGFUSE_PUBLIC_KEY"):
#         return None

#     return CallbackHandler()


# phoenix_tracer_provider = setup_phoenix()

import os

from dotenv import load_dotenv

load_dotenv()

from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register(
    project_name=os.getenv("PHOENIX_PROJECT", "support-agent-dev"),
    endpoint=os.getenv(
        "PHOENIX_COLLECTOR_ENDPOINT",
        "http://localhost:6006/v1/traces",
    ),
    protocol="http/protobuf",
    auto_instrument=False,
    set_global_tracer_provider=False,
)

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
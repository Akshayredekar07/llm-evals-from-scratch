import sys
from pathlib import Path

from dotenv import load_dotenv

# Running this file directly puts ``scripts/`` on sys.path, not the project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

load_dotenv()

from app.agent.tracing import tracer_provider

tracer = tracer_provider.get_tracer(__name__)

with tracer.start_as_current_span("manual-phoenix-test") as span:
    span.set_attribute("test.message", "Phoenix tracing works")

print("Manual trace sent to Phoenix")

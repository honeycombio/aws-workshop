import uuid
from datetime import datetime, timezone

from strands import Agent, tool
from strands.telemetry import StrandsTelemetry

StrandsTelemetry().setup_otlp_exporter()


@tool
def current_time() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@tool
def word_count(text: str) -> int:
    """Counts the number of words in the provided text."""
    return len(text.split())


session_id = str(uuid.uuid4())

agent = Agent(
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    tools=[current_time, word_count],
    system_prompt="You are a concise workshop assistant. Use your tools when asked about the time or word counts.",
    trace_attributes={
        "gen_ai.conversation.id": session_id,
        "gen_ai.agent.name": "workshop-agent",
    },
)

print(f"conversation id: {session_id}")
while True:
    try:
        user_input = input("\nyou> ")
    except EOFError:
        break
    if user_input.strip().lower() in ("exit", "quit"):
        break
    agent(user_input)
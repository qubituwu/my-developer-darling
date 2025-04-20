from typing import Literal
from AgentServices.assistant_agent import agent

# Define supported personas and their traits
PERSONAS = {
    "shy": {"style": "gentle, hesitant, humble"},
    "assertive": {"style": "confident, direct, bold"},
    "silly": {"style": "playful, humorous, quirky"},
}

def generate_feedback(code_snippet: str, persona: Literal["shy", "assertive", "silly"]) -> str:
    """
    Generate emotionally styled feedback on a code snippet based on the selected persona.
    """
    if persona not in PERSONAS:
        raise ValueError(f"Unsupported persona: {persona}")

    style = PERSONAS[persona]["style"]

    prompt = (
        f"You're a code review assistant who gives feedback in a {style} tone.\n"
        f"Here's the code to review:\n\n"
        f"{code_snippet}\n\n"
        f"Please suggest improvements, best practices, or style tips. Format it as a friendly comment."
    )

    response = agent.run(prompt)

    # Dummy feedback for now
    feedback = (
        f"[{persona.upper()} MODE] 🌟\n{response}"
    )

    return feedback

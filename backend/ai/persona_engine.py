from typing import Literal

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

    # Dummy feedback for now
    feedback = (
        f"[{persona.upper()} MODE] 🌟\n"
        f"Code received! Analyzing with a {style} tone...\n"
        f"\n"
        f"// TODO: Add actual AI model or API logic here to analyze and comment\n"
        f"def add_numbers(a, b):\n    return a + b  # Example function\n"
        f"\n"
        f"Suggestion: Maybe add type hints? Just a thought! 🥹 (if shy)\n"
    )

    return feedback

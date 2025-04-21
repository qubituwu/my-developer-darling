from typing import Literal
from AgentServices.assistant_agent import stream_graph_updates

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

    response = stream_graph_updates(code_snippet)

    # Dummy feedback for now
    feedback = (
        f"[{persona.upper()} MODE] 🌟\n{response}"
    )

    return feedback

code_snippet = (
    '''
    def chatbot(state: State):
        messages = [prompt] + state["messages"]
        return {"messages": [llm.invoke(messages)]}
    '''
)

print(generate_feedback(code_snippet, "shy"))
print(generate_feedback(code_snippet, "assertive"))
print(generate_feedback(code_snippet, "silly"))
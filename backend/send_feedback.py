from ai.AgentServices.assistant_agent import stream_graph_updates


def stream_graph_updates(prompt: str, user_input: str):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input},
    ]
    config = {
        "thread_id": "feedback-session"
    }

    for event in graph.stream({"messages": messages}, config=config):
        for value in event.values():
            last_msg = value["messages"][-1]
            return last_msg["content"]

# Call the function down here:
response_text = stream_graph_updates("You're a silly assistant.", "print(123)")
print(response_text)

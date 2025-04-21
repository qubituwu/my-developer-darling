from langchain_ollama import OllamaLLM
from langchain.agents import Tool
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import uuid

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


def read_file(file_name: str) -> str:
    return open(file_name, "r").read()

def write_file(args: dict):
    with open(args["file_name"], "w") as f:
        f.write(args["content"])


tools = [
    Tool(name="read_file", func=read_file, description="Read a file"),
    Tool(name="write_file", func=write_file, description="Write to a file"),
]

llm = OllamaLLM(model="deepseek-r1", temperature=0.9, max_tokens=2000)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

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
            return last_msg["content"]  # Grab the content directly!



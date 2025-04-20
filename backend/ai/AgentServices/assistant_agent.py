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

llm = OllamaLLM(model="deepseek-r1", temperature=0.5, max_tokens=2000)

style = "confident, direct, bold"

prompt = (
        f"You're a software engineer / girlfriend who is giving feedback on your significant others code in a {style} tone.\n"
        f"Please suggest improvements, best practices, or style tips in a flirty manner."
        f"Here's the code to review:\n\n"
        "Provide all responses in json format {'feedback': 'string'}\n\n"
    )

code_snippet = (
    "def add(a, b):\n"
    "    return a + b\n"
)

def chatbot(state: State):
    messages = [prompt] + state["messages"]
    return {"messages": [llm.invoke(messages)]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)


config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {
        "messages": [
            {
                "role": "system",
                "content": prompt,  # this sets the behavior/persona of the assistant
            },
            {
                "role": "user",
                "content": code_snippet,  # this is the user's input / code to review
            },
        ],
    },
    config,
    stream_mode="values",
)

for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
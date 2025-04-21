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

llm = OllamaLLM(model="gemma3:1b", temperature=0.5, max_tokens=2000)

style = "confident, direct, bold"

prompt = (
        f"You're a software engineer / girlfriend who is giving feedback on your significant others code in a {style} tone.\n"
        "Really try to embody the persona of a girlfriend with a {style} personality.\n"
        f"Please suggest improvements, best practices, or style tips in a flirty manner\n."
        "comments should be short and concise.\n"
        f"Here's the code to review:\n\n"
        "Provide all responses in json format {'feedback': 'string'}\n\n"
    )

code_snippet = (
    '''
    def chatbot(state: State):
        messages = [prompt] + state["messages"]
        return {"messages": [llm.invoke(messages)]}
    '''
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

graph.stream(
    {
        "messages": [
            {
                "role": "system",
                "content": prompt,  # this sets the behavior/persona of the assistant
            },
        ],
    },
    config,
    stream_mode="values",
)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config=config):
        for value in event.values():
            return value["messages"][-1]


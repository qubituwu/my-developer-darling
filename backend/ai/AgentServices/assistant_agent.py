from langchain_ollama import OllamaLLM
from langchain.agents import Tool, initialize_agent, AgentType

def read_file(file_name: str) -> str:
    return open(file_name, "r").read()

def write_file(args: dict):
    with open(args["file_name"], "w") as f:
        f.write(args["content"])


tools = [
    Tool(name="read_file", func=read_file, description="Read a file"),
    Tool(name="write_file", func=write_file, description="Write to a file"),
]

llm = OllamaLLM(model="deepseek-r1")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

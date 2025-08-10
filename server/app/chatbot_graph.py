# chatbot_graph.py

from typing import TypedDict
from typing_extensions import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

class State(TypedDict):
    messages: Annotated[list, add_messages]

load_dotenv()

llm = init_chat_model("openai:gpt-4.1")

# Define node
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# LangGraph setup
def build_chatbot_graph():
    workflow = StateGraph(State)
    workflow.add_node("chatbot", chatbot)
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    return workflow.compile()

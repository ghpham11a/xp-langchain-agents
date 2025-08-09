# chatbot_graph.py

from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

class State(TypedDict):
    messages: List[BaseMessage]

load_dotenv()

# Prompt + LLM
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = prompt | llm | StrOutputParser()

# Define node
def call_model(state):
    print(f"call_model received state: {state}")
    messages = state.get("messages", [])
    if not messages:
        return {"messages": [AIMessage(content="No message received")]}
    
    last_message = messages[-1]
    print(f"Processing message: {last_message.content}")
    
    try:
        response = chain.invoke({"question": last_message.content})
        print(f"LLM response: {response}")
    except Exception as e:
        print(f"Error calling LLM: {e}")
        response = f"Error: {str(e)}"
    
    # Return a new state with the appended message
    return {"messages": messages + [AIMessage(content=response)]}

# LangGraph setup
def build_chatbot_graph():
    workflow = StateGraph(State)
    workflow.add_node("call_model", call_model)
    workflow.set_entry_point("call_model")
    workflow.add_edge("call_model", END)
    return workflow.compile()

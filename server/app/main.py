from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from chatbot_graph import build_chatbot_graph
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_chatbot_graph()

# Simple LangChain setup (without LangGraph)
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
simple_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
simple_chain = simple_prompt | simple_llm | StrOutputParser()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/test-chat")
async def test_chat(request: Request):
    """Simple test endpoint that doesn't use LangGraph"""
    body = await request.json()
    question = body.get("question", "")
    
    async def test_generator():
        yield f"Echo: {question}"
    
    return EventSourceResponse(test_generator())

@app.post("/simple-chat")
async def simple_chat(request: Request):
    """Direct LangChain endpoint without LangGraph"""
    body = await request.json()
    question = body.get("question", "")
    print(f"Simple chat received: {question}")
    
    async def simple_generator():
        try:
            # Use async streaming
            async for chunk in simple_chain.astream({"question": question}):
                print(f"Chunk: {chunk}")
                yield chunk
        except Exception as e:
            print(f"Error in simple chat: {e}")
            yield f"Error: {str(e)}"
    
    return EventSourceResponse(simple_generator())

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question", "")
    print(f"Received question: {question}")

    if not question:
        return {"error": "No question provided."}

    initial_state = {
        "messages": [HumanMessage(content=question)]
    }

    async def event_generator():
        print("Starting event generator...")
        try:        
            async for chunk in graph.astream({"question": question}):
                print(f"Chunk: {chunk}")
                yield chunk
        except Exception as e:
            print(f"Error in event generator: {e}")
            import traceback
            traceback.print_exc()
            yield f"Error: {str(e)}"

    return EventSourceResponse(event_generator())
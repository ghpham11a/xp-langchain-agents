from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from chatbot_graph import build_chatbot_graph
from dotenv import load_dotenv, find_dotenv


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

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question", "")

    if not question:
        return {"error": "No question provided."}

    async def event_generator():
        try:
            async for chunk in graph.astream({"messages": [{"role": "user", "content": question}]}, stream_mode="messages"):
                # Handle different chunk formats
                if isinstance(chunk, tuple) and len(chunk) == 2:
                    # This is the format: (AIMessageChunk, metadata_dict)
                    msg_chunk, metadata = chunk
                    content = getattr(msg_chunk, "content", "")
                elif isinstance(chunk, dict) and "chatbot" in chunk:
                    # Original format
                    msg = chunk["chatbot"]["messages"][-1]
                    content = getattr(msg, "content", "")
                else:
                    # Direct message chunk
                    content = getattr(chunk, "content", "") if hasattr(chunk, "content") else ""
                
                # Only yield non-empty content
                if content:
                    yield {"event": "message", "data": content}
            
            # Send done signal after all chunks processed
            yield {"event": "done", "data": "[DONE]"}
        except Exception as e:
            print(f"Error in event_generator: {e}")
            yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())
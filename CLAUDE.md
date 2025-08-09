# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack chat application with a Next.js frontend and FastAPI backend that integrates LangChain/LangGraph for AI-powered conversations. The architecture uses Server-Sent Events (SSE) for real-time streaming responses.

## Development Commands

### Frontend (client/)
```bash
cd client
npm install           # Install dependencies
npm run dev          # Start dev server on localhost:3000 (with Turbopack)
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Backend (server/)
```bash
cd server
pip install -r requirements.txt                    # Install dependencies
python -m uvicorn app.main:app --reload --port 8000  # Run server on localhost:8000
```

## Architecture

### Client-Server Communication
- Frontend runs on `http://localhost:3000`
- Backend runs on `http://localhost:8000`
- Uses POST requests with JSON payloads
- Responses stream via Server-Sent Events (SSE)
- CORS configured for localhost:3000

### Backend Endpoints
- `POST /chat` - LangGraph implementation with state management
- `POST /simple-chat` - Direct LangChain streaming without LangGraph
- `POST /test-chat` - Echo endpoint for testing SSE

### Key Components

**Frontend (client/src/app/page.tsx)**
- Main chat UI with message history
- SSE client for streaming responses
- Endpoint selector for testing different backends
- Dark mode support via Tailwind CSS

**Backend (server/app/)**
- `main.py` - FastAPI server with three chat endpoints
- `chatbot_graph.py` - LangGraph workflow implementation
- Uses GPT-3.5-turbo via OpenAI API

### State Management
LangGraph uses a `State` TypedDict with a `messages` field containing a list of `BaseMessage` objects. The graph workflow processes incoming messages and appends AI responses.

## Environment Setup

### Required Environment Variables
Create `.env` file in server/ directory:
```
OPENAI_API_KEY=your-api-key-here
```

### SSE Data Format
The backend sends plain text data after "data: " prefix. The client parses SSE lines and extracts content directly (not JSON).

## Common Issues & Solutions

### Messages not sending
1. Check OPENAI_API_KEY is set in server/.env
2. Verify both servers are running (ports 3000 and 8000)
3. Use the endpoint selector to test with "/test-chat" first
4. Check browser console and server logs for errors

### LangGraph streaming issues
The LangGraph implementation expects at least 2 messages (user + AI) before yielding content. Use `/simple-chat` endpoint for direct LangChain streaming if LangGraph has issues.

## Testing Flow
1. Start with `/test-chat` endpoint to verify SSE connection
2. Switch to `/simple-chat` for basic LangChain functionality
3. Use `/chat` for full LangGraph implementation with state

## Code Style
- Frontend: TypeScript with React functional components
- Backend: Python with type hints where applicable
- Use existing patterns when adding new features
- SSE responses should yield plain strings, not JSON objects
#!/usr/bin/env python
"""Test script to verify your environment setup"""

import os
import sys
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

def test_setup():
    print("=" * 50)
    print("TESTING ENVIRONMENT SETUP")
    print("=" * 50)
    
    # Check OpenAI API Key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in environment")
        print("\nTo fix this:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Edit the .env file in the server directory")
        print("3. Replace 'your-openai-api-key-here' with your actual API key")
        return False
    elif api_key == "your-openai-api-key-here":
        print("[ERROR] OPENAI_API_KEY is still set to placeholder value")
        print("\nTo fix this:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Edit the .env file in the server directory")
        print("3. Replace 'your-openai-api-key-here' with your actual API key")
        return False
    else:
        print(f"[OK] OPENAI_API_KEY found: {api_key[:8]}...")
        
    # Test OpenAI connection
    print("\nTesting OpenAI connection...")
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        response = llm.invoke("Say 'Hello, API is working!'")
        print(f"[OK] OpenAI API is working! Response: {response.content}")
        return True
    except Exception as e:
        print(f"[ERROR] Error connecting to OpenAI: {e}")
        if "api_key" in str(e).lower():
            print("\nMake sure your API key is valid and has credits.")
        return False

if __name__ == "__main__":
    print("\n")
    success = test_setup()
    print("\n" + "=" * 50)
    if success:
        print("[OK] ALL TESTS PASSED! Your setup is ready.")
        print("\nYou can now run the server with:")
        print("  python -m uvicorn app.main:app --reload --port 8000")
    else:
        print("[ERROR] SETUP INCOMPLETE - Please fix the issues above")
    print("=" * 50)
    print("\n")
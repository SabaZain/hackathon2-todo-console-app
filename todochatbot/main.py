"""
Main application file for Todo AI Chatbot API.

This module creates and configures the FastAPI application, loads environment variables,
and starts the server with the chatbot endpoints.
"""

import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add the current directory to the Python path to resolve relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from api.chat_endpoint import get_router

# Create the FastAPI application instance
app = FastAPI(
    title="Todo AI Chatbot API",
    version="1.0.0",
    description="AI-powered chatbot for todo management with natural language processing"
)

# Configure CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Additional port for development
        "http://127.0.0.1:3001",
        "https://hackathon2-todo-console-app-frontend.onrender.com",
        "https://hackathon2-todo-console-app-qu73.vercel.app",
        # Add your frontend URL here if deployed elsewhere
        "*"  # Allow all origins during development - tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow JWT tokens to be passed through
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include the chat API routes
app.include_router(get_router(), prefix="/api")

# Simple root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint that provides a simple welcome message.

    Returns a welcome message to confirm the API is running.
    """
    return {
        "message": "Todo AI Chatbot API is running!",
        "version": "1.0.0",
        "endpoints": [
            "/api/{user_id}/chat - POST to send chat messages",
            "/api/{user_id}/conversations - GET user conversations",
            "/api/{user_id}/conversations/{conversation_id} - GET specific conversation",
            "/api/{user_id}/conversations/{conversation_id} - DELETE conversation",
            "/api/{user_id}/health - GET health check"
        ]
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint that confirms the API is operational.

    Returns a simple status message indicating the API is healthy.
    """
    return {"status": "healthy", "api": "Todo AI Chatbot API"}

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")

    print(f"Starting Todo AI Chatbot API on {host}:{port}")
    print(f"Environment variables loaded:")
    print(f"  - DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
    print(f"  - JWT_SECRET: {'SET' if os.getenv('JWT_SECRET') else 'NOT SET'}")
    print(f"  - COHERE_API_KEY: {'SET' if os.getenv('COHERE_API_KEY') else 'NOT SET'}")

    # Log database connection info
    db_url = os.getenv('DATABASE_URL', '')
    if 'postgresql' in db_url.lower():
        print("  - Connected to PostgreSQL (Neon) successfully")
    elif 'sqlite' in db_url.lower():
        print("  - WARNING: Using SQLite (should be PostgreSQL for production)")
    else:
        print("  - Database type unknown")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
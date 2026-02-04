from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from db import engine
from routes import tasks
from routes import auth


# Create the FastAPI application instance
app = FastAPI(
    title="Todo App API",
    version="1.0.0",
    description="A secure todo application API with JWT authentication, user isolation, and AI chatbot integration"
)

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://hackathon2-todo-console-app-frontend.onrender.com",
    "https://hackathon2-todo-console-app-qu73.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose the authorization header to allow JWT tokens to be passed through
    expose_headers=["Authorization"]
)


# Event handler that runs when the application starts up
@app.on_event("startup")
async def on_startup():
    """
    Initialize the database tables when the application starts.

    This function creates all database tables based on the SQLModel models
    defined in the application. It runs automatically when the app starts.
    """
    # Create all database tables based on the models
    SQLModel.metadata.create_all(bind=engine)


# Include the auth routes under the /api/auth path
# The routes/auth.py module handles user registration and authentication
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Include the task routes under the /api/tasks path
# The routes/tasks.py module handles authentication and ownership enforcement
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

# Include the chatbot API routes
try:
    from api.chat_endpoint import get_router as get_chat_router
    chat_router = get_chat_router()
    app.include_router(chat_router, prefix="/api", tags=["chatbot"])
    print("Chatbot API routes included successfully")
except ImportError as e:
    print(f"ERROR: Could not import chatbot API: {e}")
    print("Note: Chatbot functionality will not be available")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"UNEXPECTED ERROR importing chatbot API: {e}")
    print("Note: Chatbot functionality will not be available")
    import traceback
    traceback.print_exc()


# Simple root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint that provides a simple welcome message.

    Returns a welcome message to confirm the API is running.
    """
    return {"message": "Welcome to the Todo App API!", "version": "1.0.0"}


# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint that confirms the API is operational.

    Returns a simple status message indicating the API is healthy.
    """
    return {"status": "healthy", "api": "Todo App API"}

# Health check endpoint under API path for Vercel compatibility
@app.get("/api/health")
def api_health_check():
    """
    Health check endpoint that confirms the API is operational.

    Returns a simple status message indicating the API is healthy.
    """
    return {"status": "healthy", "api": "Todo App API"}


# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.

    Returns a 500 Internal Server Error response for unexpected errors.
    """
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )
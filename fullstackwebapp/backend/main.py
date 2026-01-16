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
    description="A secure todo application API with JWT authentication and user isolation"
)

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "https://hackathon2-todo-console-app-lazz.vercel.app",
    "https://hackathon2-todo-console-app-qu73.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
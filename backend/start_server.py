#!/usr/bin/env python3
"""
Backend startup script to ensure proper initialization order and avoid import conflicts.
"""

import sys
import os

# Add the backend directory to the Python path first to ensure consistent imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add the project root directory as well
project_root = os.path.dirname(backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """Main entry point for the backend application."""
    try:
        # Import the main app after setting up paths
        from main import app

        # Print startup message
        print("Backend started successfully!")
        print("Available endpoints:")
        print("  - GET / (root)")
        print("  - GET /health")
        print("  - GET /api/health")
        print("  - POST /api/auth/register")
        print("  - POST /api/auth/login")
        print("  - GET /api/auth/me")
        print("  - GET /api/tasks/")
        print("  - POST /api/tasks/")
        print("  - GET /api/tasks/{task_id}")
        print("  - PUT /api/tasks/{task_id}")
        print("  - DELETE /api/tasks/{task_id}")
        print("  - PATCH /api/tasks/{task_id}/complete")
        print("  - POST /api/{user_id}/chat")
        print("  - GET /api/{user_id}/conversations")
        print("  - GET /api/{user_id}/conversations/{conversation_id}")
        print("  - DELETE /api/{user_id}/conversations/{conversation_id}")
        print("  - GET /api/{user_id}/history")

        return app

    except Exception as e:
        print(f"Error starting backend: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app = main()

    # Run with uvicorn if called directly
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("Uvicorn not found. Install it with: pip install uvicorn[standard]")
        print("Or run with: python -m uvicorn main:app --reload")
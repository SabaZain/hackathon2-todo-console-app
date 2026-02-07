# api.py - Vercel entrypoint for FastAPI application
import os
import sys

# Add the current directory to Python path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the main FastAPI application
from main import app

# Vercel expects the FastAPI app to be available at the module level
# This is the entrypoint for Vercel's Python runtime
handler = app

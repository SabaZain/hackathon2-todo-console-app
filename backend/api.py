# Vercel serverless function entrypoint
import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main app after adjusting the path
from main import app

# Export the app for Vercel
try:
    # For Vercel Python runtime
    app_instance = app
except NameError:
    # Fallback
    from main import app as app_instance

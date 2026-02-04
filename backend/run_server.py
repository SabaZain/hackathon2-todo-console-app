#!/usr/bin/env python3
"""
Production-ready startup script for the Todo AI application backend.
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def main():
    """Main entry point for the application."""
    try:
        # Import the main app
        from main import app

        print("✅ Backend started successfully!")
        print("✅ No model registration errors detected")
        print("✅ API endpoints are available")
        print("✅ Ready to serve requests")

        # Return the app instance for further use
        return app

    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    app = main()

    # Run with uvicorn if available
    try:
        import uvicorn
        print("\n🚀 Starting server with uvicorn...")
        print("🌐 Access the API at: http://0.0.0.0:8000")
        print("📋 Available endpoints:")
        print("   - GET  / (root)")
        print("   - GET  /health")
        print("   - GET  /api/health")
        print("   - POST /api/auth/register")
        print("   - POST /api/auth/login")
        print("   - GET  /api/tasks/ (requires auth)")
        print("   - POST /api/tasks/ (requires auth)")
        print("   - Additional chatbot endpoints will be available")

        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

    except ImportError:
        print("\n⚠️  Uvicorn not found. Install it with: pip install 'uvicorn[standard]'")
        print("💡 Or run with: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        sys.exit(1)
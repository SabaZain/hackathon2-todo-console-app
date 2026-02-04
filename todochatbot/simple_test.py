import uvicorn
from main import app

print("Starting server on 127.0.0.1:8000")
print("Press Ctrl+C to stop")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False
    )
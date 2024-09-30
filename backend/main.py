import uvicorn
from src.server import initialize_application

app = initialize_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
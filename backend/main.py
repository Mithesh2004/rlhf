from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database.mongodb import MongoDB
from services.chatbot_service import ChatbotService
from routes import conversations, chat, feedback
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting backend server...")
    MongoDB.connect()
    ChatbotService.get_instance()
    print("✅ Backend ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down backend...")
    MongoDB.close()
    print("✅ Backend stopped!")


# Create FastAPI app
app = FastAPI(
    title="ICMR Diagnostic API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversations.router)
app.include_router(chat.router)
app.include_router(feedback.router)


@app.get("/")
async def root():
    return {
        "message": "ICMR Diagnostic API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "mongodb": MongoDB._db is not None,
        "chatbot": ChatbotService._instance is not None,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )

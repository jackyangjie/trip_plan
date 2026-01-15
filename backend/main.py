from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Configuration will be loaded later
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Travel Planner Backend...")
    yield
    # Shutdown
    print("Shutting down Travel Planner Backend...")


app = FastAPI(
    title="Travel Planner API",
    description="API for Travel Planner Application",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "travel-planner-api"}


# API routes will be added here
# from api.v1 import router
# app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import jwt
import hashlib

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Travel Planner API started")
    yield
    print("👋 Travel Planner API stopped")


app = FastAPI(
    title="Travel Planner API",
    description="AI-powered travel planning assistant API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

        return {"user_id": user_id, "email": email}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/auth/register")
async def register(user_data: dict):
    password_hash = hashlib.sha256(user_data["password"].encode()).hexdigest()
    user = {
        "email": user_data["email"],
        "password_hash": password_hash,
        "nickname": user_data.get("nickname", user_data["email"].split("@")[0]),
    }

    return {"message": "User created successfully", "user_id": "test-user-id"}


@app.post("/auth/login")
async def login(email: str, password: str):
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if (
        email != "test@example.com"
        or password_hash != hashlib.sha256("password".encode()).hexdigest()
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = jwt.encode(
        {
            "sub": "test-user-id",
            "email": email,
            "exp": datetime.utcnow() + access_token_expires,
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return {"access_token": access_token}


@app.get("/trips")
async def get_trips(current_user: dict = Depends(get_current_user)):
    return []


@app.post("/trips")
async def create_trip(trip_data: dict, current_user: dict = Depends(get_current_user)):
    trip_data["user_id"] = current_user["user_id"]
    return trip_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

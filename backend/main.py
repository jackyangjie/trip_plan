from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import jwt
import hashlib
import uuid

from config import settings
from app.database import get_db, init_db
from app.db_models import User, Trip
from app.api_models import TripPlanRequest
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Travel Planner API started")
    print("📦 Initializing database...")
    init_db()
    print("✅ Database initialized")
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
    db: Session = Depends(get_db),
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
async def register(user_data: dict, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data["email"]).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    password_hash = hashlib.sha256(user_data["password"].encode()).hexdigest()
    user = User(
        id=str(uuid.uuid4()),
        email=user_data["email"],
        password_hash=password_hash,
        nickname=user_data.get("nickname", user_data["email"].split("@")[0]),
        preferences=user_data.get("preferences", {}),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully", "user_id": user.id}


@app.post("/auth/login")
async def login(user_data: dict, db: Session = Depends(get_db)):
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password required")

    user = db.query(User).filter(User.email == email).first()

    if not user or user.password_hash != hashlib.sha256(password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = jwt.encode(
        {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + access_token_expires,
        },
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return {"access_token": access_token, "user_id": user.id}


@app.get("/trips")
async def get_trips(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    trips = db.query(Trip).filter(Trip.user_id == user_id).all()

    result = []
    for trip in trips:
        result.append(
            {
                "id": trip.id,
                "user_id": trip.user_id,
                "title": trip.title,
                "destinations": trip.destinations,
                "start_date": trip.start_date.isoformat() if trip.start_date else None,
                "end_date": trip.end_date.isoformat() if trip.end_date else None,
                "travelers": trip.travelers,
                "status": trip.status,
                "budget": trip.budget,
                "preferences": trip.preferences,
                "itinerary": trip.itinerary,
                "share_token": trip.share_token,
                "is_public": trip.is_public,
                "created_at": trip.created_at.isoformat() if trip.created_at else None,
                "updated_at": trip.updated_at.isoformat() if trip.updated_at else None,
            }
        )

    return result


@app.post("/trips")
async def create_trip(
    trip_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.db_models import generate_share_token

    trip = Trip(
        id=str(uuid.uuid4()),
        user_id=current_user["user_id"],
        title=trip_data.get("title", "New Trip"),
        destinations=trip_data.get("destinations", []),
        start_date=datetime.fromisoformat(trip_data["start_date"])
        if trip_data.get("start_date")
        else None,
        end_date=datetime.fromisoformat(trip_data["end_date"])
        if trip_data.get("end_date")
        else None,
        travelers=trip_data.get("travelers", 2),
        status=trip_data.get("status", "draft"),
        budget=trip_data.get("budget", {}),
        preferences=trip_data.get("preferences", {}),
        itinerary=trip_data.get("itinerary", []),
        share_token=generate_share_token(),
        is_public=trip_data.get("is_public", False),
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip created successfully",
        "trip_id": trip.id,
        "trip": {
            "id": trip.id,
            "user_id": trip.user_id,
            "title": trip.title,
            "destinations": trip.destinations,
            "start_date": trip.start_date.isoformat() if trip.start_date else None,
            "end_date": trip.end_date.isoformat() if trip.end_date else None,
            "travelers": trip.travelers,
            "status": trip.status,
            "budget": trip.budget,
            "preferences": trip.preferences,
            "itinerary": trip.itinerary,
            "share_token": trip.share_token,
            "is_public": trip.is_public,
            "created_at": trip.created_at.isoformat() if trip.created_at else None,
            "updated_at": trip.updated_at.isoformat() if trip.updated_at else None,
        },
    }


@app.get("/trips/{trip_id}")
async def get_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["user_id"]
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    return {
        "id": trip.id,
        "user_id": trip.user_id,
        "title": trip.title,
        "destinations": trip.destinations,
        "start_date": trip.start_date.isoformat() if trip.start_date else None,
        "end_date": trip.end_date.isoformat() if trip.end_date else None,
        "travelers": trip.travelers,
        "status": trip.status,
        "budget": trip.budget,
        "preferences": trip.preferences,
        "itinerary": trip.itinerary,
        "share_token": trip.share_token,
        "is_public": trip.is_public,
        "created_at": trip.created_at.isoformat() if trip.created_at else None,
        "updated_at": trip.updated_at.isoformat() if trip.updated_at else None,
    }


@app.put("/trips/{trip_id}")
async def update_trip(
    trip_id: str,
    trip_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["user_id"]
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    if "title" in trip_data:
        trip.title = trip_data["title"]
    if "destinations" in trip_data:
        trip.destinations = trip_data["destinations"]
    if "start_date" in trip_data:
        trip.start_date = datetime.fromisoformat(trip_data["start_date"])
    if "end_date" in trip_data:
        trip.end_date = datetime.fromisoformat(trip_data["end_date"])
    if "travelers" in trip_data:
        trip.travelers = trip_data["travelers"]
    if "status" in trip_data:
        trip.status = trip_data["status"]
    if "budget" in trip_data:
        trip.budget = trip_data["budget"]
    if "preferences" in trip_data:
        trip.preferences = trip_data["preferences"]
    if "itinerary" in trip_data:
        trip.itinerary = trip_data["itinerary"]

    trip.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip updated successfully",
        "trip_id": trip.id,
    }


@app.delete("/trips/{trip_id}")
async def delete_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user["user_id"]
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    db.delete(trip)
    db.commit()

    return {"message": "Trip deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi.responses import StreamingResponse
import json
import asyncio
import os
import logging
from app.db_models import generate_share_token

logger = logging.getLogger(__name__)


@app.post("/trips/ai-plan")
async def ai_plan_trip_streaming(
    trip_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Multi-Agent Trip Planning with SSE Streaming
    Uses AgentScope ReActAgents with amap-mcp-server tools.
    """
    from app.agentscope_agents.coordinator import AgentCoordinator
    from app.agentscope_agents.mcp_config import create_amap_mcp_client
    from app.ai_providers import get_provider_config

    async def ai_plan_generator(trip_data, current_user, db):
        step_data = {
            "step": 1,
            "message": "正在初始化行程...",
            "action": "init",
            "progress": 5,
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        trip = Trip(
            id=str(uuid.uuid4()),
            user_id=current_user["user_id"],
            title=trip_data.get("title", "AI 规划行程"),
            destinations=trip_data.get("destinations", []),
            start_date=datetime.fromisoformat(trip_data["start_date"])
            if trip_data.get("start_date")
            else None,
            end_date=datetime.fromisoformat(trip_data["end_date"])
            if trip_data.get("end_date")
            else None,
            travelers=trip_data.get("travelers", 2),
            status="planning",
            budget=trip_data.get("budget", {}),
            preferences=trip_data.get("preferences", {}),
            itinerary=[],
            share_token=generate_share_token(),
            is_public=False,
        )

        db.add(trip)
        db.commit()
        db.refresh(trip)

        step_data = {
            "step": 2,
            "message": "✅ 行程基础信息已创建",
            "action": "init_complete",
            "progress": 10,
            "trip_id": trip.id,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 3,
            "message": "🤖 正在初始化多智能体系统...",
            "action": "initializing_agents",
            "progress": 15,
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        ai_config = get_provider_config("openai")
        model_configs = {
            "transport": ai_config,
            "accommodation": ai_config,
            "attraction": ai_config,
            "food": ai_config,
            "budget": ai_config,
            "planner": ai_config,
        }

        mcp_client = None
        if os.getenv("AMAP_API_KEY"):
            try:
                mcp_client = create_amap_mcp_client()
                logger.info("Amap MCP client created successfully")
            except Exception as e:
                logger.warning(f"Failed to create Amap MCP client: {e}")

        coordinator = AgentCoordinator(model_configs)
        await coordinator.initialize(mcp_clients={"amap": mcp_client} if mcp_client else None)

        await asyncio.sleep(0.5)

        step_data = {
            "step": 4,
            "message": "🚄 正在搜索最佳交通方式...",
            "action": "transport",
            "progress": 30,
            "agent": "TransportAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        transport_result = await coordinator._execute_agent(
            coordinator._agents["transport"],
            {"action": "recommend", "trip_data": trip_data},
            "transport"
        )

        step_data = {
            "step": 4,
            "message": "✅ 交通推荐完成",
            "action": "transport_complete",
            "progress": 40,
            "data": transport_result,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 5,
            "message": "🏨 正在为您寻找住宿...",
            "action": "accommodation",
            "progress": 50,
            "agent": "AccommodationAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        accommodation_result = await coordinator._execute_agent(
            coordinator._agents["accommodation"],
            {"action": "recommend", "trip_data": trip_data},
            "accommodation"
        )

        step_data = {
            "step": 5,
            "message": "✅ 住宿推荐完成",
            "action": "accommodation_complete",
            "progress": 60,
            "data": accommodation_result,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 6,
            "message": "🏛️ 正在搜索精选景点...",
            "action": "attraction",
            "progress": 70,
            "agent": "AttractionAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        attraction_result = await coordinator._execute_agent(
            coordinator._agents["attraction"],
            {"action": "recommend", "trip_data": trip_data},
            "attraction"
        )

        step_data = {
            "step": 6,
            "message": "✅ 景点推荐完成",
            "action": "attraction_complete",
            "progress": 80,
            "data": attraction_result,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 7,
            "message": "🍜 正在为您推荐美食...",
            "action": "food",
            "progress": 85,
            "agent": "FoodAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        food_result = await coordinator._execute_agent(
            coordinator._agents["food"],
            {"action": "recommend", "trip_data": trip_data},
            "food"
        )

        step_data = {
            "step": 7,
            "message": "✅ 美食推荐完成",
            "action": "food_complete",
            "progress": 90,
            "data": food_result,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 8,
            "message": "💰 正在分析预算分配...",
            "action": "budget",
            "progress": 95,
            "agent": "BudgetAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        budget_result = await coordinator._execute_agent(
            coordinator._agents["budget"],
            {
                "action": "analyze",
                "transport": transport_result,
                "accommodation": accommodation_result,
                "attractions": attraction_result,
                "food": food_result,
                "budget": trip_data.get("budget", {}),
            },
            "budget"
        )

        step_data = {
            "step": 8,
            "message": "✅ 预算分析完成",
            "action": "budget_complete",
            "progress": 98,
            "data": budget_result,
        }
        yield f"data: {json.dumps(step_data)}\n\n"
        await asyncio.sleep(0.5)

        step_data = {
            "step": 9,
            "message": "📋 正在生成完整行程安排...",
            "action": "generate",
            "progress": 99,
            "agent": "PlannerAgent",
        }
        yield f"data: {json.dumps(step_data)}\n\n"

        final_plan = await coordinator._execute_agent(
            coordinator._agents["planner"],
            {
                "action": "generate_itinerary",
                "trip_data": trip_data,
                "transport_recommendations": transport_result,
                "accommodation_recommendations": accommodation_result,
                "attraction_recommendations": attraction_result,
                "food_recommendations": food_result,
                "budget_analysis": budget_result
            },
            "planner"
        )

        if "itinerary" in final_plan:
            trip.itinerary = final_plan["itinerary"]

        if "budget" in final_plan:
            trip.budget = final_plan["budget"]

        db.commit()

        await asyncio.sleep(0.5)

        step_data = {
            "step": 10,
            "message": "🎉 AI 行程规划完成！",
            "action": "complete",
            "progress": 100,
            "trip": {
                "id": trip.id,
                "title": trip.title,
                "destinations": trip.destinations,
                "start_date": trip.start_date.isoformat() if trip.start_date else None,
                "end_date": trip.end_date.isoformat() if trip.end_date else None,
                "travelers": trip.travelers,
                "status": trip.status,
                "budget": trip.budget,
                "preferences": trip.preferences,
                "itinerary": trip.itinerary,
                "share_token": trip.share_token,
                "is_public": trip.is_public,
                "created_at": trip.created_at.isoformat() if trip.created_at else None,
                "updated_at": trip.updated_at.isoformat() if trip.updated_at else None,
            },
        }
        yield f"data: {json.dumps(step_data)}\n\n"

    return StreamingResponse(
        ai_plan_generator(trip_data, current_user, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

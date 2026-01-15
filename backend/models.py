from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class TripStatus(str, Enum):
    planning = "planning"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class AgentType(str, Enum):
    planner = "planner"
    transport = "transport"
    accommodation = "accommodation"
    attraction = "attraction"
    food = "food"
    budget = "budget"


class SessionStatus(str, Enum):
    active = "active"
    completed = "completed"


class TripBudget(BaseModel):
    total: int
    transport: int = 0
    accommodation: int = 0
    food: int = 0
    activities: int = 0


class User(BaseModel):
    id: str
    email: str
    nickname: Optional[str] = None
    preferences: dict = {}


class Trip(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    title: str
    destinations: List[str]
    start_date: str
    end_date: str
    budget: TripBudget
    status: TripStatus = TripStatus.planning
    itinerary: List[dict] = []
    share_token: Optional[str] = None
    is_public: bool = False


class TripCreate(BaseModel):
    title: str
    destinations: List[str]
    start_date: str
    end_date: str
    budget: TripBudget
    travelers: int = 2
    preferences: dict = {}

from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class TripPlanRequest(BaseModel):
    """Request model for trip planning"""

    title: str
    destinations: List[str]
    start_date: str
    end_date: str
    travelers: int = 2
    budget: Dict[str, Any]
    preferences: Dict[str, Any] = {}


class TripResponse(BaseModel):
    """Response model for trip planning result"""

    id: str
    title: str
    destinations: List[str]
    start_date: str
    end_date: str
    travelers: int
    status: str
    itinerary: List[Dict[str, Any]]
    budget: Dict[str, Any]


class RecommendationResponse(BaseModel):
    """Model for agent recommendations"""

    transport: Dict[str, Any]
    accommodation: Dict[str, Any]
    attractions: Dict[str, Any]
    food: Dict[str, Any]

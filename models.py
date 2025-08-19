from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserPreferences(BaseModel):
    origin: str
    budget: float
    start_date: date
    end_date: date
    interests: List[str]  # e.g., ["beach", "culture", "food"]
    max_destinations: Optional[int] = 3

class Destination(BaseModel):
    name: str
    country: str
    description: str
    estimated_cost: float

class ItineraryItem(BaseModel):
    day: int
    activity: str
    location: str
    cost: float

class TripPlan(BaseModel):
    destinations: List[Destination]
    itinerary: List[ItineraryItem]
    total_cost: float
    cost_breakdown: dict  # e.g., {"flights": 500, "hotels": 300, "activities": 200}

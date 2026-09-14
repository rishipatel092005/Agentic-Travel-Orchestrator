"""
Itinerary models for trip planning.
Defines the structure of activities, daily plans, and complete itineraries.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Activity(BaseModel):
    """
    Individual activity within a day plan.
    
    Represents a single activity with location, cost, and characteristics.
    """
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Activity name (e.g., 'Visit Eiffel Tower')"
    )
    
    category: str = Field(
        ...,
        description="Activity category (e.g., 'sightseeing', 'dining', 'adventure')"
    )
    
    estimated_cost: float = Field(
        default=0.0,
        ge=0,
        description="Estimated cost in currency units"
    )
    
    is_outdoor: bool = Field(
        default=False,
        description="Whether the activity is outdoors"
    )
    
    latitude: Optional[float] = Field(
        default=None,
        ge=-90,
        le=90,
        description="Geographic latitude coordinate"
    )
    
    longitude: Optional[float] = Field(
        default=None,
        ge=-180,
        le=180,
        description="Geographic longitude coordinate"
    )
    
    duration_minutes: Optional[int] = Field(
        default=None,
        ge=15,
        description="Estimated duration in minutes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Eiffel Tower Visit",
                "category": "sightseeing",
                "estimated_cost": 30.0,
                "is_outdoor": True,
                "latitude": 48.8584,
                "longitude": 2.2945,
                "duration_minutes": 120
            }
        }


class DayPlan(BaseModel):
    """
    Daily plan containing multiple activities.
    Represents a single day's itinerary.
    """
    
    day: int = Field(
        ...,
        gt=0,
        description="Day number (1-indexed)"
    )
    
    activities: List[Activity] = Field(
        default_factory=list,
        description="List of activities for this day"
    )
    
    estimated_daily_cost: float = Field(
        default=0.0,
        ge=0,
        description="Estimated total cost for the day"
    )
    
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes for the day (e.g., 'Rain expected')"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "day": 1,
                "activities": [
                    {
                        "name": "Breakfast",
                        "category": "dining",
                        "estimated_cost": 15.0
                    },
                    {
                        "name": "Eiffel Tower",
                        "category": "sightseeing",
                        "estimated_cost": 30.0
                    }
                ],
                "estimated_daily_cost": 45.0,
                "notes": "Start early to avoid crowds"
            }
        }


class Itinerary(BaseModel):
    """
    Complete itinerary for a trip.
    Contains all day plans and cost estimates.
    """
    
    destination: str = Field(
        ...,
        description="Trip destination"
    )
    
    day_plans: List[DayPlan] = Field(
        default_factory=list,
        description="List of daily plans"
    )
    
    estimated_total_cost: float = Field(
        default=0.0,
        ge=0,
        description="Total estimated cost for the entire trip"
    )
    
    accommodation_cost: float = Field(
        default=0.0,
        ge=0,
        description="Total accommodation cost"
    )
    
    transportation_cost: float = Field(
        default=0.0,
        ge=0,
        description="Total transportation cost"
    )
    
    activity_cost: float = Field(
        default=0.0,
        ge=0,
        description="Total activity cost"
    )
    
    meal_cost: float = Field(
        default=0.0,
        ge=0,
        description="Total meal cost"
    )
    
    contingency_fund: float = Field(
        default=0.0,
        ge=0,
        description="Emergency/contingency budget"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Paris",
                "day_plans": [],
                "estimated_total_cost": 0.0,
                "accommodation_cost": 0.0,
                "transportation_cost": 0.0,
                "activity_cost": 0.0,
                "meal_cost": 0.0,
                "contingency_fund": 0.0
            }
        }

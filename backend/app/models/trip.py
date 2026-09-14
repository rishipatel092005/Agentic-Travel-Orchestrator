"""
Trip request model with validation.
Defines the structure of a trip planning request.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class TripRequest(BaseModel):
    """
    Trip planning request model.
    
    Validates user input for trip parameters including:
    - Destination name
    - Duration in days
    - Number of travelers
    - Total budget
    - User interests/preferences
    - Maximum daily travel time
    """
    
    destination: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Travel destination (e.g., 'Paris', 'Tokyo')"
    )
    
    days: int = Field(
        ...,
        gt=0,
        le=365,
        description="Number of days for the trip"
    )
    
    travelers: int = Field(
        ...,
        gt=0,
        le=50,
        description="Number of travelers"
    )
    
    budget: float = Field(
        ...,
        gt=0,
        description="Total budget in currency units"
    )
    
    interests: List[str] = Field(
        ...,
        min_length=1,
        max_length=20,
        description="List of user interests (e.g., ['adventure', 'culture', 'food'])"
    )
    
    max_daily_travel_minutes: int = Field(
        default=180,
        ge=30,
        le=1440,
        description="Maximum daily travel time in minutes (default: 180 min / 3 hours)"
    )
    
    @field_validator("destination")
    @classmethod
    def validate_destination(cls, v: str) -> str:
        """Ensure destination is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("Destination cannot be empty or whitespace")
        return v.strip()
    
    @field_validator("interests")
    @classmethod
    def validate_interests(cls, v: List[str]) -> List[str]:
        """Ensure interests are valid and cleaned."""
        if not v:
            raise ValueError("At least one interest is required")
        
        # Remove duplicates and convert to lowercase
        cleaned = [interest.strip().lower() for interest in v if interest.strip()]
        
        if not cleaned:
            raise ValueError("Interests cannot be empty after validation")
        
        return list(set(cleaned))  # Remove duplicates
    
    @field_validator("budget")
    @classmethod
    def validate_budget(cls, v: float) -> float:
        """Ensure budget is reasonable."""
        if v > 1_000_000:
            raise ValueError("Budget seems unreasonably high. Please check the value.")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "destination": "Paris",
                "days": 5,
                "travelers": 2,
                "budget": 3000.0,
                "interests": ["culture", "food", "history"],
                "max_daily_travel_minutes": 180
            }
        }

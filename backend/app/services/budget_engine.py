"""
Budget calculation engine for trip planning.
Pure Python business logic for deterministic cost calculations.
No LLM calls - only arithmetic.
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.models.itinerary import Itinerary, DayPlan, Activity


class BudgetValidationResult(BaseModel):
    """Result of budget validation."""
    
    estimated_total: float = Field(
        description="Total estimated cost for the trip"
    )
    user_budget: float = Field(
        description="User's stated budget"
    )
    over_budget: bool = Field(
        description="Whether the itinerary exceeds the budget"
    )
    difference: float = Field(
        description="Difference between budget and cost (positive = under budget)"
    )
    within_budget: bool = Field(
        description="Whether the itinerary is within budget"
    )
    percentage_used: float = Field(
        description="Percentage of budget used (0-100)"
    )


class BudgetEngine:
    """
    Deterministic budget calculation engine.
    Handles all cost calculations for itineraries without external dependencies.
    """
    
    # Default daily costs per person (in currency units)
    DEFAULT_MEAL_COST_PER_DAY = 60.0
    DEFAULT_ACCOMMODATION_COST_PER_NIGHT = 100.0
    DEFAULT_TRANSPORTATION_COST_PER_DAY = 20.0
    CONTINGENCY_PERCENTAGE = 0.10  # 10% of total
    
    def __init__(
        self,
        meal_cost_per_day: float = DEFAULT_MEAL_COST_PER_DAY,
        accommodation_per_night: float = DEFAULT_ACCOMMODATION_COST_PER_NIGHT,
        transportation_per_day: float = DEFAULT_TRANSPORTATION_COST_PER_DAY
    ):
        """
        Initialize budget engine with cost parameters.
        
        Args:
            meal_cost_per_day: Daily meal cost per person
            accommodation_per_night: Nightly accommodation cost per person
            transportation_per_day: Daily transportation cost per person
        """
        self.meal_cost_per_day = meal_cost_per_day
        self.accommodation_per_night = accommodation_per_night
        self.transportation_per_day = transportation_per_day
    
    def calculate_meal_cost(self, days: int, travelers: int) -> float:
        """
        Calculate total meal cost.
        
        Args:
            days: Number of days in the trip
            travelers: Number of travelers
            
        Returns:
            Total meal cost
        """
        return self.meal_cost_per_day * days * travelers
    
    def calculate_accommodation_cost(self, days: int, travelers: int) -> float:
        """
        Calculate total accommodation cost.
        Assumes nights = days - 1 (leave on day N, sleep N-1 nights).
        
        Args:
            days: Number of days in the trip
            travelers: Number of travelers
            
        Returns:
            Total accommodation cost
        """
        nights = max(0, days - 1)  # Don't count travel day as full night
        return self.accommodation_per_night * nights * travelers
    
    def calculate_transportation_cost(self, days: int, travelers: int) -> float:
        """
        Calculate total transportation cost.
        
        Args:
            days: Number of days in the trip
            travelers: Number of travelers
            
        Returns:
            Total transportation cost
        """
        return self.transportation_per_day * days * travelers
    
    def calculate_activity_cost(self, activities: list[Activity]) -> float:
        """
        Calculate total activity cost from a list of activities.
        
        Args:
            activities: List of Activity objects
            
        Returns:
            Sum of all activity costs
        """
        return sum(activity.estimated_cost for activity in activities)
    
    def calculate_itinerary_cost(
        self,
        itinerary: Itinerary,
        days: int,
        travelers: int
    ) -> tuple[float, dict]:
        """
        Calculate complete itinerary cost breakdown.
        
        Args:
            itinerary: Itinerary object
            days: Number of days
            travelers: Number of travelers
            
        Returns:
            Tuple of (total_cost, cost_breakdown)
        """
        # Calculate base costs
        meal_cost = self.calculate_meal_cost(days, travelers)
        accommodation_cost = self.calculate_accommodation_cost(days, travelers)
        transportation_cost = self.calculate_transportation_cost(days, travelers)
        
        # Calculate activity costs from day plans
        activity_cost = 0.0
        for day_plan in itinerary.day_plans:
            activity_cost += self.calculate_activity_cost(day_plan.activities)
        
        # Subtotal before contingency
        subtotal = meal_cost + accommodation_cost + transportation_cost + activity_cost
        
        # Calculate contingency fund (10% of subtotal)
        contingency_fund = subtotal * self.CONTINGENCY_PERCENTAGE
        
        # Total cost
        total_cost = subtotal + contingency_fund
        
        # Cost breakdown
        breakdown = {
            "meal_cost": meal_cost,
            "accommodation_cost": accommodation_cost,
            "transportation_cost": transportation_cost,
            "activity_cost": activity_cost,
            "subtotal": subtotal,
            "contingency_fund": contingency_fund,
            "total_cost": total_cost
        }
        
        return total_cost, breakdown
    
    def validate_budget(
        self,
        itinerary: Itinerary,
        days: int,
        travelers: int,
        user_budget: float
    ) -> BudgetValidationResult:
        """
        Validate itinerary against user's budget.
        
        Args:
            itinerary: Itinerary object to validate
            days: Number of days
            travelers: Number of travelers
            user_budget: User's budget
            
        Returns:
            BudgetValidationResult with validation details
        """
        estimated_total, _ = self.calculate_itinerary_cost(itinerary, days, travelers)
        
        difference = user_budget - estimated_total
        over_budget = estimated_total > user_budget
        within_budget = not over_budget
        percentage_used = (estimated_total / user_budget * 100) if user_budget > 0 else 0
        
        return BudgetValidationResult(
            estimated_total=round(estimated_total, 2),
            user_budget=user_budget,
            over_budget=over_budget,
            difference=round(difference, 2),
            within_budget=within_budget,
            percentage_used=round(percentage_used, 2)
        )
    
    def optimize_activity_costs(
        self,
        activities: list[Activity],
        available_budget: float
    ) -> tuple[list[Activity], float]:
        """
        Sort activities by cost efficiency (for future optimization).
        Returns activities and remaining budget.
        
        Args:
            activities: List of activities
            available_budget: Available budget for activities
            
        Returns:
            Tuple of (activities, remaining_budget)
        """
        total_activity_cost = self.calculate_activity_cost(activities)
        remaining_budget = available_budget - total_activity_cost
        
        return activities, remaining_budget

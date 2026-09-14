"""
Itinerary evaluation service.
Scores itineraries across multiple dimensions to determine quality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, ClassVar, Dict
from app.models.itinerary import Itinerary, Activity


class EvaluationScore(BaseModel):
    """
    Complete evaluation score for an itinerary.
    Contains individual dimension scores and overall weighted score.
    """
    
    budget_score: float = Field(
        ge=0, le=100,
        description="Budget alignment score (0-100)"
    )
    preference_score: float = Field(
        ge=0, le=100,
        description="User preference alignment score (0-100)"
    )
    activity_diversity_score: float = Field(
        ge=0, le=100,
        description="Activity diversity score (0-100)"
    )
    weather_score: float = Field(
        default=50.0,
        ge=0, le=100,
        description="Weather suitability score (0-100) - not yet implemented"
    )
    travel_efficiency_score: float = Field(
        default=50.0,
        ge=0, le=100,
        description="Travel efficiency score (0-100) - not yet implemented"
    )
    
    # Weights for scoring (must sum to 1.0)
    # ClassVar for Pydantic v2 compatibility
    WEIGHTS: ClassVar[Dict[str, float]] = {
        "budget": 0.30,
        "preferences": 0.25,
        "weather": 0.20,
        "travel_efficiency": 0.15,
        "activity_diversity": 0.10
    }
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score."""
        return (
            self.budget_score * self.WEIGHTS["budget"] +
            self.preference_score * self.WEIGHTS["preferences"] +
            self.weather_score * self.WEIGHTS["weather"] +
            self.travel_efficiency_score * self.WEIGHTS["travel_efficiency"] +
            self.activity_diversity_score * self.WEIGHTS["activity_diversity"]
        )
    
    class Config:
        json_schema_extra = {
            "example": {
                "budget_score": 85.0,
                "preference_score": 90.0,
                "activity_diversity_score": 75.0,
                "weather_score": 50.0,
                "travel_efficiency_score": 50.0
            }
        }


class EvaluationService:
    """
    Service for evaluating itineraries across multiple dimensions.
    Provides scoring and recommendations.
    """
    
    def __init__(self):
        """Initialize evaluation service."""
        pass
    
    def evaluate_budget_score(
        self,
        estimated_cost: float,
        user_budget: float
    ) -> float:
        """
        Score the itinerary based on budget alignment.
        
        Scoring logic:
        - 100: Cost is <= 80% of budget (good buffer)
        - 85: Cost is 80-90% of budget
        - 70: Cost is 90-100% of budget
        - 50: Cost is 100-110% of budget (slightly over)
        - 0: Cost exceeds 110% of budget (significantly over)
        
        Args:
            estimated_cost: Estimated total cost
            user_budget: User's budget
            
        Returns:
            Score from 0-100
        """
        if user_budget <= 0:
            return 50.0  # Neutral score if no budget provided
        
        percentage = (estimated_cost / user_budget) * 100
        
        if percentage <= 80:
            return 100.0
        elif percentage <= 90:
            return 85.0
        elif percentage <= 100:
            return 70.0
        elif percentage <= 110:
            return 50.0
        else:
            return 0.0
    
    def evaluate_preference_score(
        self,
        user_interests: List[str],
        activities: List[Activity]
    ) -> float:
        """
        Score the itinerary based on user preference alignment.
        
        Scoring logic:
        - Checks how many activities match user interests
        - 100: 100% of activities match interests or >80% match
        - 80: 60-80% of activities match interests
        - 60: 40-60% of activities match interests
        - 40: 20-40% of activities match interests
        - 20: 0-20% of activities match interests
        
        Args:
            user_interests: List of user interests
            activities: List of activities in itinerary
            
        Returns:
            Score from 0-100
        """
        if not activities or not user_interests:
            return 50.0  # Neutral if no data
        
        user_interests_lower = [interest.lower() for interest in user_interests]
        matches = 0
        
        for activity in activities:
            activity_category = activity.category.lower()
            # Check if activity category matches any user interest
            if any(interest in activity_category or activity_category in interest 
                   for interest in user_interests_lower):
                matches += 1
        
        match_percentage = (matches / len(activities)) * 100
        
        if match_percentage >= 80:
            return 100.0
        elif match_percentage >= 60:
            return 80.0
        elif match_percentage >= 40:
            return 60.0
        elif match_percentage >= 20:
            return 40.0
        else:
            return 20.0
    
    def evaluate_activity_diversity_score(
        self,
        activities: List[Activity],
        days: int
    ) -> float:
        """
        Score based on diversity of activity categories.
        
        Scoring logic:
        - More unique categories = higher score
        - Minimum 2 unique categories for good score
        - One activity per day on average for good score
        
        Args:
            activities: List of activities
            days: Number of days in trip
            
        Returns:
            Score from 0-100
        """
        if not activities or days <= 0:
            return 0.0
        
        # Count unique categories
        categories = set(activity.category.lower() for activity in activities)
        unique_category_count = len(categories)
        
        # Activities per day ratio
        activities_per_day = len(activities) / days
        
        # Score based on diversity and density
        # Target: 3-5 activities per day, 4-6 unique categories
        category_score = min((unique_category_count / 5) * 100, 100.0)
        density_score = min(activities_per_day / 5 * 100, 100.0)
        
        # Average the two scores
        diversity_score = (category_score * 0.6 + density_score * 0.4)
        
        return min(diversity_score, 100.0)
    
    def evaluate_itinerary(
        self,
        itinerary: Itinerary,
        user_interests: List[str],
        user_budget: float,
        days: int
    ) -> EvaluationScore:
        """
        Perform complete itinerary evaluation.
        
        Args:
            itinerary: Itinerary to evaluate
            user_interests: User's stated interests
            user_budget: User's budget
            days: Number of days
            
        Returns:
            EvaluationScore with all dimension scores
        """
        # Collect all activities
        all_activities = []
        for day_plan in itinerary.day_plans:
            all_activities.extend(day_plan.activities)
        
        # Calculate individual scores
        budget_score = self.evaluate_budget_score(
            itinerary.estimated_total_cost,
            user_budget
        )
        
        preference_score = self.evaluate_preference_score(
            user_interests,
            all_activities
        )
        
        activity_diversity_score = self.evaluate_activity_diversity_score(
            all_activities,
            days
        )
        
        # Create evaluation result
        evaluation = EvaluationScore(
            budget_score=round(budget_score, 2),
            preference_score=round(preference_score, 2),
            activity_diversity_score=round(activity_diversity_score, 2)
        )
        
        return evaluation
    
    def should_replan(self, score: EvaluationScore) -> bool:
        """
        Determine if an itinerary should be replanned.
        
        Replanning recommended if:
        - Overall score < 50, or
        - Budget score < 30 (significantly over budget), or
        - Preference score < 40 (poor interest match)
        
        Args:
            score: EvaluationScore to evaluate
            
        Returns:
            True if replanning is recommended
        """
        return (
            score.overall_score < 50 or
            score.budget_score < 30 or
            score.preference_score < 40
        )
    
    def get_improvement_recommendations(self, score: EvaluationScore) -> List[str]:
        """
        Get recommendations for improving the itinerary.
        
        Args:
            score: EvaluationScore to analyze
            
        Returns:
            List of improvement recommendations
        """
        recommendations = []
        
        if score.budget_score < 60:
            recommendations.append(
                "Consider reducing activity costs or accommodation options"
            )
        
        if score.preference_score < 60:
            recommendations.append(
                "Add more activities matching your stated interests"
            )
        
        if score.activity_diversity_score < 50:
            recommendations.append(
                "Increase variety in activity types and categories"
            )
        
        if not recommendations:
            recommendations.append("Itinerary looks great! No immediate improvements needed.")
        
        return recommendations

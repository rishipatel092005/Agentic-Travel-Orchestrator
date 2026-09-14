"""
FastAPI application for Agentic Travel Planner backend.
Provides REST API endpoints for trip planning and validation.
"""

from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel, Field
from langgraph.errors import GraphRecursionError

# Allow the compatibility route to reuse the existing root-level agent package.
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agent.agentic_workflow import GraphBuilder
from agent.agentic_workflow import get_travel_graph, invoke_travel_graph
from app.config import settings
from app.database import db
from app.models.trip import TripRequest
from app.models.itinerary import Itinerary, DayPlan
from app.services.budget_engine import BudgetEngine
from app.services.evaluation import EvaluationService


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Agentic Travel Planner Backend API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
budget_engine = BudgetEngine()
evaluation_service = EvaluationService()
travel_graph = get_travel_graph(model_provider="groq")


class QueryRequest(BaseModel):
    """Natural-language request sent by the existing Streamlit client."""

    question: str = Field(..., min_length=1)


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    db.close()
    logger.info("Application shutdown")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns application status and database connectivity.
    """
    db_status = "connected" if db.is_connected() else "disconnected"
    
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": "0.1.0",
        "database": db_status
    }


@app.post("/api/trips/validate")
async def validate_trip(trip_request: TripRequest):
    """
    Validate trip request and calculate basic itinerary metrics.
    
    This endpoint:
    1. Validates the trip request using Pydantic
    2. Creates a basic itinerary structure
    3. Calculates budget breakdown
    4. Evaluates itinerary quality
    5. Returns validation result
    
    Args:
        trip_request: TripRequest model with trip parameters
        
    Returns:
        Dictionary with validation results, budget breakdown, and evaluation scores
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        logger.info(f"Validating trip to {trip_request.destination}")
        
        # Create basic itinerary structure
        itinerary = Itinerary(
            destination=trip_request.destination,
            day_plans=[
                DayPlan(day=i, activities=[])
                for i in range(1, trip_request.days + 1)
            ]
        )
        
        # Calculate budget
        estimated_total, cost_breakdown = budget_engine.calculate_itinerary_cost(
            itinerary,
            trip_request.days,
            trip_request.travelers
        )
        
        # Validate budget
        budget_result = budget_engine.validate_budget(
            itinerary,
            trip_request.days,
            trip_request.travelers,
            trip_request.budget
        )
        
        # Evaluate itinerary (with empty activities for now)
        evaluation_score = evaluation_service.evaluate_itinerary(
            itinerary,
            trip_request.interests,
            trip_request.budget,
            trip_request.days
        )
        
        # Check if replanning is needed
        needs_replan = evaluation_service.should_replan(evaluation_score)
        recommendations = evaluation_service.get_improvement_recommendations(evaluation_score)
        
        # Prepare response
        response = {
            "success": True,
            "message": "Trip request validated successfully",
            "trip_details": {
                "destination": trip_request.destination,
                "days": trip_request.days,
                "travelers": trip_request.travelers,
                "interests": trip_request.interests,
                "max_daily_travel_minutes": trip_request.max_daily_travel_minutes
            },
            "budget_analysis": {
                "user_budget": budget_result.user_budget,
                "estimated_total": budget_result.estimated_total,
                "within_budget": budget_result.within_budget,
                "over_budget": budget_result.over_budget,
                "difference": budget_result.difference,
                "percentage_used": budget_result.percentage_used
            },
            "cost_breakdown": cost_breakdown,
            "evaluation_scores": {
                "budget_score": evaluation_score.budget_score,
                "preference_score": evaluation_score.preference_score,
                "activity_diversity_score": evaluation_score.activity_diversity_score,
                "weather_score": evaluation_score.weather_score,
                "travel_efficiency_score": evaluation_score.travel_efficiency_score,
                "overall_score": round(evaluation_score.overall_score, 2)
            },
            "recommendations": {
                "needs_replan": needs_replan,
                "suggestions": recommendations
            }
        }
        
        logger.info(f"Trip validation successful: {trip_request.destination}")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during trip validation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during trip validation"
        )


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    """Run the existing LangGraph travel agent for the Streamlit client."""
    try:
        if not settings.groq_api_key or not settings.groq_api_key.strip():
            raise HTTPException(
                status_code=503,
                detail="GROQ_API_KEY is missing. Add it to backend/.env and restart the backend."
            )

        output = invoke_travel_graph(travel_graph, query.question)

        if isinstance(output, dict) and output.get("messages"):
            final_message = output["messages"][-1]
            answer = getattr(final_message, "content", str(final_message))
        else:
            answer = str(output)

        return {"answer": answer}
    except HTTPException:
        raise
    except GraphRecursionError:
        logger.exception("Travel agent workflow exceeded its iteration limit")
        raise HTTPException(
            status_code=504,
            detail="The travel agent needed more tool steps than allowed. Please try a shorter or more specific request.",
        )
    except Exception as error:
        logger.exception("Travel agent request failed")
        if "429" in str(error) or "rate_limit" in str(error).lower():
            raise HTTPException(
                status_code=503,
                detail="The model provider is rate-limited. Please retry shortly.",
            )
        raise HTTPException(
            status_code=502,
            detail=(
                "The travel agent request failed with "
                f"{type(error).__name__}. Verify the Groq key, quota, and network connection."
            )
        )


@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "message": "Welcome to Agentic Travel Planner API",
        "endpoints": {
            "health": "/health",
            "validate_trip": "POST /api/trips/validate"
        },
        "documentation": "/docs"
    }

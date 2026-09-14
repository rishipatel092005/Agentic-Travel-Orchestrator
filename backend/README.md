# Agentic Travel Planner - Backend Foundation

This is the backend foundation for the Agentic Travel Planner application.

## Project Structure

```
backend/
└── app/
    ├── __init__.py              # Package initialization
    ├── main.py                  # FastAPI application and endpoints
    ├── config.py                # Configuration and environment variables
    ├── database.py              # MongoDB connection management
    ├── models/
    │   ├── __init__.py
    │   ├── trip.py              # TripRequest model with validation
    │   └── itinerary.py         # Activity, DayPlan, Itinerary models
    └── services/
        ├── __init__.py
        ├── budget_engine.py     # Pure Python cost calculation logic
        └── evaluation.py        # Itinerary evaluation and scoring
```

## File Responsibilities

### `main.py`
- FastAPI application initialization
- CORS middleware configuration
- `/health` endpoint - checks app and database status
- `POST /api/trips/validate` - validates trip requests and calculates metrics
- Error handling and logging

### `config.py`
- Settings management using `pydantic-settings`
- Loads environment variables from `.env`
- Optional API keys (fail gracefully if not provided)
- Never exposes secrets in responses or logs

### `database.py`
- MongoDB connection using `pymongo`
- Singleton pattern for connection management
- Collections: `users`, `trips`, `itineraries`
- Connection testing and offline mode support
- Lazy initialization (only connects when needed)

### `models/trip.py`
- `TripRequest` Pydantic model
- Validates: destination, days, travelers, budget, interests
- Default values for optional fields
- Custom validators for data cleaning and validation

### `models/itinerary.py`
- `Activity` - individual activity with location and cost
- `DayPlan` - collection of activities for one day
- `Itinerary` - complete trip with day plans and cost breakdown

### `services/budget_engine.py`
- Deterministic cost calculations (NO LLM)
- Methods for:
  - Meal cost calculation
  - Accommodation cost calculation
  - Transportation cost calculation
  - Activity cost calculation
  - Total itinerary cost with breakdown
  - Budget validation
- Default daily costs (configurable)
- 10% contingency fund calculation
- `BudgetValidationResult` structure

### `services/evaluation.py`
- Multi-dimensional itinerary evaluation
- Scoring dimensions:
  - **Budget score** (30%): Alignment with user's budget
  - **Preference score** (25%): Match with user interests
  - **Activity diversity** (10%): Variety in activities
  - **Weather score** (20%): Placeholder for future
  - **Travel efficiency** (15%): Placeholder for future
- `EvaluationScore` with weighted overall score
- Replanning recommendations based on scores

## Setup Instructions

### 1. Install Dependencies

The required packages are already installed in your environment. If needed:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
- Set `MONGODB_URI` if using MongoDB
- Add API keys as needed (optional for development)

### 3. Run the Backend

From the **root directory** of the project:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "application": "Agentic Travel Planner",
  "version": "0.1.0",
  "database": "connected"
}
```

### Validate Trip Request

```bash
curl -X POST http://localhost:8000/api/trips/validate \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "days": 5,
    "travelers": 2,
    "budget": 3000.0,
    "interests": ["culture", "food", "history"],
    "max_daily_travel_minutes": 180
  }'
```

Response example:
```json
{
  "success": true,
  "message": "Trip request validated successfully",
  "trip_details": {
    "destination": "Paris",
    "days": 5,
    "travelers": 2,
    "interests": ["culture", "food", "history"],
    "max_daily_travel_minutes": 180
  },
  "budget_analysis": {
    "user_budget": 3000.0,
    "estimated_total": 2590.0,
    "within_budget": true,
    "over_budget": false,
    "difference": 410.0,
    "percentage_used": 86.33
  },
  "cost_breakdown": {
    "meal_cost": 600.0,
    "accommodation_cost": 800.0,
    "transportation_cost": 100.0,
    "activity_cost": 0.0,
    "subtotal": 1500.0,
    "contingency_fund": 150.0,
    "total_cost": 1650.0
  },
  "evaluation_scores": {
    "budget_score": 100.0,
    "preference_score": 50.0,
    "activity_diversity_score": 0.0,
    "weather_score": 50.0,
    "travel_efficiency_score": 50.0,
    "overall_score": 66.5
  },
  "recommendations": {
    "needs_replan": false,
    "suggestions": ["Itinerary looks great! No immediate improvements needed."]
  }
}
```

## Import Structure

```
backend/
  app/
    main.py          → imports from config, database, models, services
    config.py        → imports pydantic_settings
    database.py      → imports pymongo, config
    models/
      trip.py        → imports pydantic
      itinerary.py   → imports pydantic
    services/
      budget_engine.py   → imports from models.itinerary, pydantic
      evaluation.py      → imports from models.itinerary, pydantic
```

## Required Packages

Add to `requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
pymongo==4.6.0
python-dotenv==1.0.0
```

## Common Issues & Debugging

### Issue: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run from the `backend` directory:
```bash
cd backend
uvicorn app.main:app --reload
```

### Issue: `MongoDB connection refused`

**Solutions**:
1. Ensure MongoDB is running: `mongod`
2. Check `MONGODB_URI` in `.env`
3. App will work in offline mode if MongoDB is unavailable (with warnings)

### Issue: `Validation error on trip request`

**Check**:
- Destination must be non-empty string
- Days must be > 0
- Travelers must be > 0
- Budget must be > 0
- Interests must have at least one item
- max_daily_travel_minutes must be 30-1440

### Issue: Import errors in models or services

**Solution**: Verify:
- You're in the `backend` directory
- All `__init__.py` files exist in folders
- PYTHONPATH includes the backend folder

### Issue: `.env` file not being read

**Solution**:
1. Create `.env` file in `backend/` directory (not root)
2. File must have `key=value` format
3. No quotes needed for string values

## Next Steps (Future Phases)

- [ ] Add LangGraph agent workflow
- [ ] Implement actual itinerary generation with activities
- [ ] Add weather API integration
- [ ] Add route optimization
- [ ] Add user authentication
- [ ] Add Redis caching
- [ ] Add WebSocket support for real-time updates
- [ ] Add Streamlit or React frontend

## Type Hints

All functions use Python type hints for clarity:
- Return types specified
- Parameter types specified
- Optional types marked with `Optional[T]`
- List types use `List[T]`

## Error Handling

- Input validation via Pydantic models
- HTTP exceptions for API errors
- Logging at INFO and ERROR levels
- Graceful database fallback

## Code Quality

- Single responsibility principle
- Clear function documentation
- No magic numbers (use constants)
- Modular and testable design
- Production-ready but beginner-friendly

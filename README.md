# Agentic Travel Planner

An AI-powered travel planning application that turns a natural-language trip request into a structured itinerary with activities, weather context, transportation suggestions, and cost estimates. The project combines a LangGraph tool-using agent with deterministic Python business logic for budget calculations and a FastAPI plus Streamlit application surface.

The current implementation supports live agent planning, INR-first budgeting, optional external travel APIs, bounded workflow execution, lightweight caching, and graceful operation when MongoDB is unavailable.

## Features

 -  Autonomous Agent Planning : 
LangGraph-powered workflow with multi-step reasoning and tool orchestration
Bounded execution: Maximum 2 tool cycles + 1 planning refinement to prevent infinite loops
Intelligent fallbacks: Graceful degradation when external services are unavailable

 - Deterministic Budget Engine : 
INR-first currency system with proper Indian number formatting (₹1,00,000 vs $100,000)
Real-time currency conversion only when explicitly requested
Dynamic cost allocation: Hotel, meal, activity, and transport pricing based on destination and travel preferences
Budget validation: Ensures recommendations stay within user constraints

 - Multi-Source Data Integration : 
Weather Intelligence: OpenWeatherMap integration with caching and timeout handling
Venue Discovery: Google Places + Tavily dual-engine place search
Currency Conversion: ExchangeRate API with INR short-circuit optimization
Transport Logistics: Real-time feasibility checks with travel-time constraints

 - Production-Grade Infrastructure : 
Cached LangGraph Instances: One compiled graph per process eliminates per-request overhead
Lightweight in-process caching: Deduplicates repeated weather, place, and currency requests
Network resilience: Connection timeouts and exponential backoff for external APIs
Optional MongoDB persistence: Works seamlessly in disconnected mode without degradation

 - Observability & Debugging: 
Comprehensive timing logs: LLM latency, tool execution, workflow duration, and total request time
Structured logging: Request/response tracing for production debugging
Health checks: Real-time database and service status monitoring

## Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Runtime** | Python 3.10+ | Core application language |
| **API Framework** | FastAPI + Uvicorn | REST API and API documentation |
| **Agent Engine** | LangGraph | Stateful agent workflow orchestration |
| **LLM** | Groq | Fast LLM inference for agent reasoning |
| **AI Framework** | LangChain | LLM and tool integrations |
| **Validation** | Pydantic v2 | Data validation and serialization |
| **UI** | Streamlit | Travel planning user interface |
| **Storage** | MongoDB | Optional trip and user persistence |
| **HTTP Clients** | Requests + HTTPX | External API communication |

## Architecture

```mermaid
flowchart TD
    User[User] --> UI[Streamlit UI]
    UI --> API[FastAPI API]

    API --> Cache[In-Process Cache]
    API --> Graph[Cached LangGraph]

    Graph --> LLM[Groq LLM]
    Graph --> Tools[Travel Tools]

    Tools --> Weather[OpenWeatherMap]
    Tools --> Places[Google Places / Tavily]
    Tools --> Currency[ExchangeRate API]
    Tools --> Math[Deterministic Python Logic]

    API --> Validation[Trip Validation & Budget Engine]
    API -. optional .-> Mongo[(MongoDB)]

    Graph --> Evaluation[Itinerary Evaluation]
    Evaluation --> Decision{Constraints Satisfied?}

    Decision -->|No| Graph
    Decision -->|Yes| Result[Final Itinerary]

    Result --> UI
```


### Request flow

1. The user submits a natural-language request in Streamlit.
2. Streamlit sends the request to `POST /query`.
3. FastAPI reuses the process-level compiled LangGraph.
4. The LLM decides whether a tool is needed.
5. External tools fetch only the information requested by the workflow.
6. Python performs arithmetic and validation deterministically.
7. The workflow returns a Markdown itinerary to the UI.

The graph is bounded to one initial agent pass plus a maximum of two tool/re-planning cycles. This prevents an unbounded tool loop.

## Project Structure

```text
Agentic-Travel-Orchestrator/
├── agent/
│   └── agentic_workflow.py       Cached LangGraph and workflow limits
├── backend/
│   └── app/
│       ├── main.py               Backend foundation API
│       ├── config.py             Pydantic settings and environment loading
│       ├── database.py           MongoDB connection and collections
│       ├── models/
│       │   ├── trip.py           Trip request validation model
│       │   └── itinerary.py      Activity, day-plan, and itinerary models
│       └── services/
│           ├── budget_engine.py  Deterministic cost calculations
│           └── evaluation.py     Itinerary scoring logic
├── config/
│   └── config.yaml               LLM provider and model configuration
├── prompt_library/
│   └── prompt.py                 Agent behavior and response-format instructions
├── tools/
│   ├── weather_info_tool.py      Weather tools with fallbacks and timing logs
│   ├── place_search_tool.py      Attraction, restaurant, activity, and transport tools
│   ├── currency_conversion_tool.py Currency conversion tool
│   └── expense_calculator_tool.py Deterministic calculation tools
├── utils/
│   ├── model_loader.py           LLM construction with timeout configuration
│   ├── weather_info.py            Weather client with timeout and caching
│   ├── place_info_search.py      Place clients with lightweight caching
│   ├── currency_converter.py     Currency client and INR short-circuit
│   └── expense_calculator.py     Arithmetic helpers and INR formatting
├── main.py                       Existing root FastAPI application
├── streamlit_app.py              Streamlit frontend
├── requirements.txt              Python dependencies
├── .env.example                  Environment-variable template
└── README.md                     Project documentation
```

## Installation and Setup

### Prerequisites

- Windows PowerShell.
- Python 3.10 or newer.
- Internet access for the configured model and external APIs.
- MongoDB only if persistence is required. The chatbot can run without it.

### 1. Open the project

```powershell
cd "C:\Users\Admin\Downloads\Agentic Travel Orchestrator"
```

### 2. Activate the virtual environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

If activation is unavailable, use the project interpreter directly:

```powershell
"C:\Users\Admin\Downloads\Agentic Travel Orchestrator\.venv\Scripts\python.exe"
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create or edit the root `.env` file:

```dotenv
GROQ_API_KEY=your_new_groq_key
OPENAI_API_KEY=
TAVILY_API_KEY=
GPLACES_API_KEY=
OPENWEATHERMAP_API_KEY=
EXCHANGE_RATE_API_KEY=
MONGODB_URI=mongodb://localhost:27017
```

The default model is configured in `config/config.yaml`. Use `TAVILY_API_KEY`, not `TAVILAY_API_KEY`.

### 5. Optional MongoDB setup

The application uses:

```text
Database: agentic_travel_planner
Collections: users, trips, itineraries
```

Without MongoDB, the API reports `database: disconnected` and continues in offline mode. Chatbot generation and deterministic trip validation still work.

## Running Locally

Use two PowerShell terminals and keep both open.

### Terminal 1: FastAPI backend

Run from the `backend` directory:

```powershell
cd C:\Users\Admin\Downloads\Agentic Travel Orchestrator\backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Terminal 2: Streamlit frontend

Run from the project root, not from `backend`:

```powershell
cd C:\Users\Admin\Downloads\Agentic Travel Orchestrator
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8501
```

Frontend URL:

```text
http://127.0.0.1:8501
```

## Usage

1. Open `http://127.0.0.1:8501`.
2. Enter a request such as:

   ```text
   Plan a 3-day trip to Goa for two people with a budget of ₹50,000. I like beaches, food, and culture.
   ```

3. Submit the form.
4. The agent gathers relevant information, performs deterministic calculations, and returns a Markdown travel plan.
5. Review the trip summary, day-wise activities, budget breakdown, total estimated cost, and budget status.

## Screenshots and Demo

### Local demo

Run the application locally and open:

```text
http://127.0.0.1:8501
```

The repository currently does not contain a deployed public demo URL. Add a verified deployment link here after deploying the application.

### Recommended repository screenshots

For a polished GitHub presentation, capture these real screens after running the project:

1. Streamlit trip request screen.
2. Generated itinerary with day-wise activities.
3. Budget breakdown and within-budget result.
4. FastAPI Swagger page at `/docs`.

Store screenshots under `docs/images/` only when you are ready to add actual product captures. Do not use placeholder screenshots or invented demo links.

## API Documentation

Interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### `GET /health`

Returns application and database status.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Example response:

```json
{
  "status": "healthy",
  "application": "Agentic Travel Planner",
  "version": "0.1.0",
  "database": "disconnected"
}
```

### `POST /query`

Runs the LangGraph travel agent.

Request body:

```json
{
  "question": "Plan a 3-day trip to Goa with a budget in INR"
}
```

PowerShell request:

```powershell
$body = @{ question = "Plan a 3-day trip to Goa with a budget in INR" } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/query -Method Post -ContentType "application/json" -Body $body
```

Success response shape:

```json
{
  "answer": "## Trip summary ...",
  "currency": "INR"
}
```

The endpoint requires a configured model API key and may use external travel tools depending on the request.

### `POST /api/trips/validate`

Validates trip input and calculates deterministic budget metrics without an LLM call.

Request body:

```json
{
  "destination": "Goa",
  "days": 3,
  "travelers": 2,
  "budget": 50000,
  "interests": ["beaches", "food", "culture"],
  "max_daily_travel_minutes": 180
}
```

PowerShell request:

```powershell
$body = @{
    destination = "Goa"
    days = 3
    travelers = 2
    budget = 50000
    interests = @("beaches", "food", "culture")
    max_daily_travel_minutes = 180
} | ConvertTo-Json

Invoke-RestMethod http://127.0.0.1:8000/api/trips/validate `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

```

## Future Enhancements

- Multi-language support (English, Hindi, Spanish)
- User preference learning (favorite destinations, repeat bookings)
- Integration with booking platforms (hotel/flight reservations)
- Real-time price tracking for flights and accommodations
- Group trip splitting and collaborative planning
- Carbon footprint estimation for eco-conscious travelers
- Container deployment (Docker and Kubernetes manifests)
- Batch processing for enterprise travel management

## About

Autonomous agent design with LangGraph
Deterministic business logic separation
Multi-service orchestration and resilience patterns
Real-world constraint handling (budgets, time, availability)

Author: Rishi Patel
Repository: github.com/rishipatel092005/Agentic-Travel-Orchestrator

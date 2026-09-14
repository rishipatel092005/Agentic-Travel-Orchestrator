from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from agent.agentic_workflow import get_travel_graph, invoke_travel_graph
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

logger = logging.getLogger(__name__)
travel_graph = get_travel_graph(model_provider="groq")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    started_at = time.perf_counter()
    try:
        output = invoke_travel_graph(travel_graph, query.question)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        logger.info("total_request_seconds=%.3f", time.perf_counter() - started_at)
        return {"answer": final_output, "currency": "INR"}
    except Exception as e:
        logger.exception("Travel query failed after %.3f seconds", time.perf_counter() - started_at)
        error_text = str(e)
        if "429" in error_text or "rate_limit" in error_text.lower():
            return JSONResponse(
                status_code=503,
                content={"error": "The model provider is rate-limited. Please retry shortly."},
            )
        return JSONResponse(status_code=500, content={"error": "Travel planning failed."})
import os
import logging
import time
from pathlib import Path
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class PlaceSearchTool:
    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.google_places_search = (
            GooglePlaceSearchTool(self.google_api_key)
            if self.google_api_key
            else None
        )
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(city: str) -> str:
            """Search attractions of a place"""
            started_at = time.perf_counter()
            if not self.google_places_search and not os.environ.get("TAVILY_API_KEY"):
                return f"Attractions unavailable for {city}: no place-search API key is configured"
            try:
                attraction_result = self.google_places_search.google_search_attractions(city)
                if attraction_result:
                    return f"Following are the attractions of {city} as suggested by google: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(city)
                result = f"Google cannot find the details due to {e}. \nFollowing are the attractions of {city}: {tavily_result}"
                logger.info("tool=search_attractions seconds=%.3f", time.perf_counter() - started_at)
                return result
        
        @tool
        def search_restaurants(city: str) -> str:
            """Search restaurants of a place"""
            started_at = time.perf_counter()
            if not self.google_places_search and not os.environ.get("TAVILY_API_KEY"):
                return f"Restaurants unavailable for {city}: no place-search API key is configured"
            try:
                restaurants_result = self.google_places_search.google_search_restaurants(city)
                if restaurants_result:
                    return f"Following are the restaurants of {city} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(city)
                result = f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {city}: {tavily_result}"
                logger.info("tool=search_restaurants seconds=%.3f", time.perf_counter() - started_at)
                return result
        
        @tool
        def search_activities(city: str) -> str:
            """Search activities of a place"""
            started_at = time.perf_counter()
            if not self.google_places_search and not os.environ.get("TAVILY_API_KEY"):
                return f"Activities unavailable for {city}: no place-search API key is configured"
            try:
                restaurants_result = self.google_places_search.google_search_activity(city)
                if restaurants_result:
                    return f"Following are the activities in and around {city} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(city)
                result = f"Google cannot find the details due to {e}. \nFollowing are the activities of {city}: {tavily_result}"
                logger.info("tool=search_activities seconds=%.3f", time.perf_counter() - started_at)
                return result
        
        @tool
        def search_transportation(city: str) -> str:
            """Search transportation of a place"""
            started_at = time.perf_counter()
            if not self.google_places_search and not os.environ.get("TAVILY_API_KEY"):
                return f"Transportation unavailable for {city}: no place-search API key is configured"
            try:
                restaurants_result = self.google_places_search.google_search_transportation(city)
                if restaurants_result:
                    return f"Following are the modes of transportation available in {city} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(city)
                result = f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {city}: {tavily_result}"
                logger.info("tool=search_transportation seconds=%.3f", time.perf_counter() - started_at)
                return result
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]
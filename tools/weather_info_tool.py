import os
import logging
import time
from pathlib import Path
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class WeatherInfoTool:
    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            started_at = time.perf_counter()
            if not self.api_key:
                return f"Weather unavailable for {city}: OPENWEATHERMAP_API_KEY is not configured"
            weather_data = self.weather_service.get_current_weather(city)
            logger.info("tool=get_current_weather seconds=%.3f", time.perf_counter() - started_at)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Could not fetch weather for {city}"
        
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            started_at = time.perf_counter()
            if not self.api_key:
                return f"Weather forecast unavailable for {city}: OPENWEATHERMAP_API_KEY is not configured"
            forecast_data = self.weather_service.get_forecast_weather(city)
            logger.info("tool=get_weather_forecast seconds=%.3f", time.perf_counter() - started_at)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {city}"
    
        return [get_current_weather, get_weather_forecast]
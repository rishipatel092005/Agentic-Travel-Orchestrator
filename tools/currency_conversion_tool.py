import os
import logging
import time
from pathlib import Path
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[1] / ".env")
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount:float, from_currency:str, to_currency:str):
            """Convert only when the user explicitly requests another currency."""
            started_at = time.perf_counter()
            if from_currency.upper() == to_currency.upper() == "INR":
                return amount
            result = self.currency_service.convert(amount, from_currency, to_currency)
            logger.info("tool=convert_currency seconds=%.3f", time.perf_counter() - started_at)
            return result
        
        return [convert_currency]
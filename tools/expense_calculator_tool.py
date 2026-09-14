from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool
import logging
import time

logger = logging.getLogger(__name__)

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def calculate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """Calculate total hotel cost"""
            started_at = time.perf_counter()
            result = self.calculator.multiply(price_per_night, total_days)
            logger.info("tool=calculate_total_hotel_cost seconds=%.3f", time.perf_counter() - started_at)
            return result
        
        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total expense of the trip"""
            started_at = time.perf_counter()
            result = self.calculator.calculate_total(*costs)
            logger.info("tool=calculate_total_expense seconds=%.3f", time.perf_counter() - started_at)
            return result
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            started_at = time.perf_counter()
            result = self.calculator.calculate_daily_budget(total_cost, days)
            logger.info("tool=calculate_daily_expense_budget seconds=%.3f", time.perf_counter() - started_at)
            return result
        
        return [calculate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]
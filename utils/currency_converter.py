import requests
from functools import lru_cache

class CurrencyConverter:
    def __init__(self, api_key: str | None):
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/" if api_key else ""
    
    @lru_cache(maxsize=128)
    def convert(self, amount: float, from_currency: str, to_currency: str):
        """Convert the amount from one currency to another"""
        if from_currency.upper() == to_currency.upper():
            return amount
        if not self.base_url:
            raise ValueError("EXCHANGE_RATE_API_KEY is not configured")
        url = f"{self.base_url}/{from_currency}"
        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            raise Exception("API call failed:", response.json())
        rates = response.json()["conversion_rates"]
        if to_currency not in rates:
            raise ValueError(f"{to_currency} not found in exchange rates.")
        return amount * rates[to_currency]
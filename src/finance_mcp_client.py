import os
import requests
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:5001")

class FinanceClient:
    def __init__(self):
        self.base_url = MCP_SERVER_URL

    def fetch_stock_data(self, ticker: str):
        url = f"{self.base_url}/tool_call"
        payload = {
            "name": "fetch_stock_data",
            "parameters": {"ticker": ticker}
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {ticker}: {e}")
            return {"error": str(e)}

    def fetch_historical_data(self, ticker: str, period: str = "1mo"):
        url = f"{self.base_url}/tool_call"
        payload = {
            "name": "fetch_historical_data",
            "parameters": {"ticker": ticker, "period": period}
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return {"error": str(e)}
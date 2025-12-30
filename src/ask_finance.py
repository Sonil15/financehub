import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from finance_mcp_client import FinanceClient

try:
    from llm_parser import TickerParser
except ImportError as e:
    print(f"Error: Failed to import TickerParser: {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Fetch financial data using stock ticker symbols or natural language")
    parser.add_argument("query", help="Stock ticker or natural language query (e.g., 'Get me Tesla data')")
    args = parser.parse_args()

    if not args.query.strip():
        print("❌ Error: Empty query")
        sys.exit(1)

    llm_parser = TickerParser()
    ticker, timeframe = llm_parser.extract_ticker_and_timeframe(args.query)
    
    if not ticker:
        print("❌ Error: Could not extract a valid stock ticker from your query")
        print("Try asking for a specific stock, e.g., 'Show me Apple stock' or just provide the ticker (e.g., 'AAPL')")
        sys.exit(1)
    
    print(f"✓ Extracted ticker: {ticker}")
    if timeframe:
        print(f"✓ Extracted timeframe: {timeframe}")

    client = FinanceClient()

    try:
        data = client.fetch_stock_data(ticker)
        
        if "error" in data:
            print(f"❌ Error: {data.get('error')}")
            sys.exit(1)
        
        historical_data = None
        if timeframe:
            hist_response = client.fetch_historical_data(ticker, timeframe)
            if "error" not in hist_response:
                historical_data = hist_response.get('data', {})
        
        print("\n✓ Financial data retrieved successfully.\n")
        
        summary = llm_parser.generate_analysis_summary(
            ticker, 
            data.get('data', {}), 
            user_query=args.query,
            historical_data=historical_data
        )
        
        if summary:
            print("📊 Analysis:\n")
            print(summary)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
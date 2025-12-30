from flask import Flask, request, jsonify
import os
import sys
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(__file__))

try:
    from data_fetchers.yahoo_finance import YahooFinanceFetcher
    logger.info("Successfully imported YahooFinanceFetcher")
except ImportError as e:
    logger.error(f"Failed to import YahooFinanceFetcher: {e}")
    logger.error(traceback.format_exc())
    YahooFinanceFetcher = None

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/tool_call", methods=["POST"])
def tool_call():
    logger.debug(f"Received request: {request.json}")
    
    if not request.json:
        logger.error("No JSON in request")
        return jsonify({"error": "invalid request"}), 400
    
    tool_name = request.json.get("name")
    parameters = request.json.get("parameters", {})
    logger.debug(f"Tool name: {tool_name}, Parameters: {parameters}")

    if tool_name == "fetch_stock_data":
        ticker = parameters.get("ticker")
        if not ticker:
            logger.error("No ticker provided")
            return jsonify({"error": "ticker parameter is required"}), 400
        
        try:
            logger.info(f"Fetching stock data for {ticker}")
            if YahooFinanceFetcher is None:
                logger.error("YahooFinanceFetcher is None")
                return jsonify({"error": "YahooFinanceFetcher not loaded"}), 500
            data = YahooFinanceFetcher.fetch_stock_price(ticker)
            logger.info(f"Successfully fetched data for {ticker}: {data}")
            return jsonify({"data": data})
        except Exception as e:
            logger.error(f"Error fetching stock price: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": str(e), "details": traceback.format_exc()}), 500
    
    elif tool_name == "fetch_historical_data":
        ticker = parameters.get("ticker")
        period = parameters.get("period", "1mo")
        
        if not ticker:
            logger.error("No ticker provided")
            return jsonify({"error": "ticker parameter is required"}), 400
        
        try:
            logger.info(f"Fetching historical data for {ticker} with period {period}")
            
            if YahooFinanceFetcher is None:
                logger.error("YahooFinanceFetcher is None")
                return jsonify({"error": "YahooFinanceFetcher not loaded"}), 500
            
            data = YahooFinanceFetcher.fetch_historical_data(ticker, period)
            logger.info(f"Successfully fetched historical data for {ticker}")
            return jsonify({"data": data})
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": str(e), "details": traceback.format_exc()}), 500
    
    else:
        logger.error(f"Unknown tool name: {tool_name}")
        return jsonify({"error": "unknown tool name"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

class YahooFinanceFetcher:
    @staticmethod
    def fetch_stock_price(ticker: str) -> dict:
        try:
            logger.info(f"Fetching stock price for {ticker} from yfinance")
            stock = yf.Ticker(ticker)
            
            # Get basic info
            info = stock.info
            logger.debug(f"Got info for {ticker}")
            
            # Extract key data with fallbacks
            price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
            
            return {
                "ticker": ticker,
                "price": float(price) if price else 0,
                "currency": info.get("currency", "USD"),
                "marketCap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "name": info.get("longName", ticker),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "description": info.get("longBusinessSummary", "N/A")[:200] if info.get("longBusinessSummary") else "N/A"
            }
        except Exception as e:
            logger.error(f"Failed to fetch stock price for {ticker}: {str(e)}")
            raise Exception(f"Failed to fetch stock price for {ticker}: {str(e)}")

    @staticmethod
    def fetch_historical_data(ticker: str, period: str = "1mo") -> dict:
        try:
            logger.info(f"Fetching historical data for {ticker} with period {period}")
            stock = yf.Ticker(ticker)
            
            # Determine interval based on period
            if period in ["1y", "2y", "5y", "10y"]:
                # Use weekly data for longer timeframes
                interval = "1wk"
                hist = stock.history(period=period, interval=interval)
                logger.info(f"Fetching {period} data with weekly interval for {ticker}")
            else:
                # Use daily data for shorter timeframes
                interval = "1d"
                hist = stock.history(period=period)
                logger.info(f"Fetching {period} data with daily interval for {ticker}")
            
            if hist.empty:
                raise Exception(f"No historical data found for {ticker}")
            
            # Convert DataFrame to JSON-serializable format
            hist_reset = hist.reset_index()
            # Convert dates to strings
            hist_reset['Date'] = hist_reset['Date'].astype(str)
            # Convert to dictionary with orient='records' for cleaner format
            hist_data = hist_reset.to_dict(orient='records')
            
            # Return appropriate number of data points based on period
            if period == "1mo":
                hist_data = hist_data[-20:]  # Last 20 daily data points
            elif period == "3mo":
                hist_data = hist_data[-40:]  # Last 40 daily data points
            elif period == "6mo":
                hist_data = hist_data[-100:]  # Last 100 daily data points
            elif period in ["1y", "2y", "5y", "10y"]:
                hist_data = hist_data[-52:]  # Last 52 weeks (approximately 1 year of weekly data)
            # For "all" or other periods, return all data
            
            return {
                "ticker": ticker,
                "period": period,
                "interval": interval,
                "rows": len(hist),
                "data": hist_data
            }
        except Exception as e:
            logger.error(f"Failed to fetch historical data for {ticker}: {str(e)}")
            raise Exception(f"Failed to fetch historical data for {ticker}: {str(e)}")

    @staticmethod
    def fetch_financials(ticker: str) -> dict:
        try:
            logger.info(f"Fetching financials for {ticker}")
            stock = yf.Ticker(ticker)
            
            return {
                "ticker": ticker,
                "financials": stock.financials.to_dict() if stock.financials is not None else {}
            }
        except Exception as e:
            logger.error(f"Failed to fetch financials for {ticker}: {str(e)}")
            raise Exception(f"Failed to fetch financials for {ticker}: {str(e)}")
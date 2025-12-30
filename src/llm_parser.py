import os
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class TickerParser:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def extract_ticker_and_timeframe(self, user_input: str) -> tuple:
        """Extract stock ticker and time period from natural language input using Groq LLM"""
        
        prompt = f"""EXTRACT ONLY - NO EXPLANATIONS

Extract the stock ticker and time period from this request.
Return EXACTLY in this format: TICKER,TIMEFRAME

Company ticker mappings:
Tesla=TSLA, Apple=AAPL, Microsoft=MSFT, Amazon=AMZN, Google=GOOGL, Alphabet=GOOGL, Meta=META, Nvidia=NVDA, John Deere=DE, Toyota=TM, Ford=F, Coca Cola=KO, McDonald's=MCD, Netflix=NFLX, Uber=UBER, Adani Ports=ADANIPORTS

Time period mappings:
past month OR this month OR 1 month=1mo
past 3 months OR quarter=3mo
past 6 months OR half year=6mo
past year OR 1 year=1y
past 2 years=2y
past 5 years=5y
No time period mentioned=NONE

User: "{user_input}"
Response: TICKER,TIMEFRAME"""
        
        try:
            logger.debug(f"Calling Groq API to extract ticker and timeframe")
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=15,
                temperature=0
            )
            response = message.choices[0].message.content.strip()
            logger.debug(f"LLM response: {response}")
            
            if not response:
                return None, None
            
            response = response.split('\n')[0].strip()
            
            if ',' not in response:
                return None, None
            
            parts = response.split(',')
            
            if len(parts) >= 2:
                ticker = parts[0].strip().upper()
                timeframe = parts[1].strip().lower()
                
                if len(ticker) > 10 or not ticker.isalnum():
                    return None, None
                
                ticker = ticker if ticker != "INVALID" else None
                timeframe = timeframe if timeframe != "none" else None
                
                logger.debug(f"Extracted ticker: {ticker}, timeframe: {timeframe}")
                return ticker, timeframe
            else:
                logger.error(f"Unexpected response format: {response}")
                return None, None
                
        except Exception as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return None, None

    def extract_ticker(self, user_input: str) -> str:
        """Extract stock ticker from natural language input using Groq LLM"""
        prompt = f"""Extract the stock ticker symbol from the user's request. 
        Return ONLY the ticker symbol (e.g., AAPL, TSLA, GOOGL) with no additional text.
        If no valid ticker is found, return 'INVALID'.
        
        User request: {user_input}
        
        Ticker:"""
        
        try:
            logger.debug(f"Calling Groq API with model {self.model}")
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0
            )
            ticker = message.choices[0].message.content.strip().upper()
            logger.debug(f"Extracted ticker: {ticker}")
            return ticker if ticker != "INVALID" else None
        except Exception as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return None

    def generate_analysis_summary(self, ticker: str, data: dict, user_query: str = None, historical_data: dict = None) -> str:
        """Generate a contextual summary of stock data based on user's query using Groq LLM"""
        # Format market cap safely
        market_cap = data.get('marketCap', 'N/A')
        if isinstance(market_cap, int):
            market_cap_str = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
        else:
            market_cap_str = str(market_cap)
        
        # Format P/E ratio safely
        pe_ratio = data.get('pe_ratio', 'N/A')
        if isinstance(pe_ratio, (int, float)) and pe_ratio != 'N/A':
            pe_ratio_str = f"{pe_ratio:.2f}"
        else:
            pe_ratio_str = str(pe_ratio)
        
        # Format price
        price = data.get('price', 0)
        if isinstance(price, (int, float)):
            price_str = f"${price:.2f}"
        else:
            price_str = str(price)
        
        user_question = user_query if user_query else 'Provide a summary of this stock.'
        
        # Build detailed prompt
        prompt = f"""{ticker} Stock Analysis

Question: {user_question}

Current Data:
- Price: {price_str}
- P/E Ratio: {pe_ratio_str}
- Market Cap: {market_cap_str}
- Sector: {data.get('sector', 'N/A')}
- Industry: {data.get('industry', 'N/A')}
"""
        
        # Add historical data if available
        if historical_data and historical_data.get('data'):
            hist_list = historical_data.get('data', [])
            if isinstance(hist_list, list) and len(hist_list) > 0:
                first_price = hist_list[0].get('Close', 0)
                last_price = hist_list[-1].get('Close', 0)
                period = historical_data.get('period', '1mo')
                
                if first_price and last_price:
                    change = ((last_price - first_price) / first_price) * 100
                    prompt += f"\nHistorical Performance ({period}): ${first_price:.2f} → ${last_price:.2f} ({change:+.1f}%)\n"
        
        prompt += f"""
Please provide a comprehensive and detailed analysis addressing the user's question. Include:
1. Direct answer to their question
2. Key metrics analysis and what they mean
3. Historical trend analysis if data is available
4. Market position and competitive context
5. Risk and opportunity assessment
6. Investment perspective (if relevant)

Be thorough, informative, and use specific data points to support your analysis."""
        
        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,  # Increased from 350 to 800
                temperature=0.3
            )
            return message.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return None
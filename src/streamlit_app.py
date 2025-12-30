import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from finance_mcp_client import FinanceClient
from llm_parser import TickerParser

# Page configuration
st.set_page_config(
    page_title="Financial Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    /* Main color scheme */
    :root {
        --primary-color: #1E88E5;
        --secondary-color: #43A047;
        --accent-color: #FB8C00;
        --dark-bg: #0F1419;
        --card-bg: #1A1F26;
        --text-primary: #E0E0E0;
        --text-secondary: #9E9E9E;
        --border-color: #2A3139;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background */
    .main {
        background: linear-gradient(135deg, #0F1419 0%, #1A1F26 100%);
        color: var(--text-primary);
    }
    
    /* Title styling */
    .header-title {
        color: var(--primary-color);
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(135deg, #1E88E5 0%, #43A047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .header-subtitle {
        color: var(--text-secondary);
        font-size: 1.1em;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: var(--card-bg) !important;
        border: 2px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid var(--primary-color) !important;
        box-shadow: 0 0 20px rgba(30, 136, 229, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 12px !important;
        font-size: 1.1em !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(30, 136, 229, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(30, 136, 229, 0.5) !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1A1F26 0%, #232A33 100%);
        border: 1px solid var(--border-color);
        padding: 25px !important;
        border-radius: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .metric-card:hover {
        border-color: var(--primary-color);
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(30, 136, 229, 0.2);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, rgba(30, 136, 229, 0.1) 0%, rgba(67, 160, 71, 0.1) 100%);
        border-left: 5px solid var(--primary-color);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: var(--text-primary);
    }
    
    /* Section headers */
    .section-header {
        color: var(--primary-color);
        font-size: 1.8em;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Data table */
    .dataframe {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
    }
    
    /* Chart styling */
    .chart-container {
        background: linear-gradient(135deg, #1A1F26 0%, #232A33 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 30px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, var(--border-color), transparent);
        margin: 40px 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0F1419 0%, #1A1F26 100%);
        border-right: 1px solid var(--border-color);
    }
    
    /* Help text */
    .help-text {
        color: var(--text-secondary);
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--primary-color) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'llm_parser' not in st.session_state:
    st.session_state.llm_parser = TickerParser()
if 'finance_client' not in st.session_state:
    st.session_state.finance_client = FinanceClient()

# Header section
st.markdown('<h1 class="header-title">📈 FinanceHub</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Intelligent Financial Analysis with AI-Powered Insights</p>', unsafe_allow_html=True)
st.markdown("---")

# Main search section
col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_input(
        "📊 Enter your financial query:",
        placeholder="e.g., 'How is Apple stock performing?' or 'Show me Tesla over the past year'",
        key="query_input"
    )

with col2:
    analyze_button = st.button("🔍 Analyze", use_container_width=True, key="analyze_btn")

st.markdown("---")

# Main analysis section
if analyze_button and user_query:
    with st.spinner("🔄 Analyzing your query..."):
        try:
            # Extract ticker and timeframe
            ticker, timeframe = st.session_state.llm_parser.extract_ticker_and_timeframe(user_query)
            
            if not ticker:
                st.error("❌ Could not extract a valid stock ticker from your query. Try being more specific!", icon="⚠️")
                st.stop()
            
            # Fetch stock data
            with st.spinner(f"📥 Fetching data for {ticker}..."):
                data = st.session_state.finance_client.fetch_stock_data(ticker)
            
            if "error" in data:
                st.error(f"❌ Error: {data.get('error')}", icon="⚠️")
                st.stop()
            
            stock_data = data.get('data', {})
            
            # Display stock header
            st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #1A1F26 0%, #232A33 100%);
                    border: 1px solid #2A3139;
                    border-radius: 16px;
                    padding: 25px;
                    margin-bottom: 30px;
                '>
                    <h2 style='color: #1E88E5; margin: 0; font-size: 2em;'>
                        {stock_data.get('name', ticker)}
                    </h2>
                    <p style='color: #9E9E9E; margin: 10px 0 0 0; font-size: 1.1em;'>
                        {ticker}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics row with premium styling
            metric_cols = st.columns(4)
            
            metrics = [
                ("Price", f"${stock_data.get('price', 'N/A'):.2f}" if isinstance(stock_data.get('price'), (int, float)) else stock_data.get('price', 'N/A'), "💰"),
                ("P/E Ratio", f"{stock_data.get('pe_ratio', 'N/A'):.2f}" if isinstance(stock_data.get('pe_ratio'), (int, float)) else stock_data.get('pe_ratio', 'N/A'), "📊"),
                ("Market Cap", f"${stock_data.get('marketCap')/1e9:.1f}B" if isinstance(stock_data.get('marketCap'), int) and stock_data.get('marketCap') > 1e9 else str(stock_data.get('marketCap', 'N/A')), "🏢"),
                ("Sector", stock_data.get('sector', 'N/A'), "🏭")
            ]
            
            for col, (label, value, emoji) in zip(metric_cols, metrics):
                with col:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <p style='color: #9E9E9E; margin: 0; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px;'>
                                {emoji} {label}
                            </p>
                            <p style='color: #1E88E5; margin: 10px 0 0 0; font-size: 1.8em; font-weight: 700;'>
                                {value}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Fetch historical data if timeframe specified
            historical_data = None
            if timeframe:
                with st.spinner(f"📈 Fetching historical data for {timeframe}..."):
                    hist_response = st.session_state.finance_client.fetch_historical_data(ticker, timeframe)
                    if "error" not in hist_response:
                        historical_data = hist_response.get('data', {})
            
            # Display historical data chart
            if historical_data and historical_data.get('data'):
                st.markdown('<h3 class="section-header">📊 Price History</h3>', unsafe_allow_html=True)
                
                hist_list = historical_data.get('data', [])
                if isinstance(hist_list, list) and len(hist_list) > 0:
                    df = pd.DataFrame(hist_list)
                    df['Date'] = pd.to_datetime(df['Date'])
                    df = df.sort_values('Date')
                    
                    # Display line chart in a styled container
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.line_chart(
                        df.set_index('Date')[['Close']],
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display data table
                    with st.expander("📋 View Detailed Historical Data"):
                        st.dataframe(
                            df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].style.format({
                                'Open': '${:,.2f}',
                                'High': '${:,.2f}',
                                'Low': '${:,.2f}',
                                'Close': '${:,.2f}',
                                'Volume': '{:,.0f}'
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
            
            st.markdown("---")
            
            # AI Analysis section
            st.markdown('<h3 class="section-header">🤖 AI Analysis</h3>', unsafe_allow_html=True)
            
            with st.spinner("✨ Generating comprehensive analysis..."):
                summary = st.session_state.llm_parser.generate_analysis_summary(
                    ticker,
                    stock_data,
                    user_query=user_query,
                    historical_data=historical_data
                )
                
                if summary:
                    st.markdown(f"""
                        <div style='
                            background: linear-gradient(135deg, #1A1F26 0%, #232A33 100%);
                            border: 1px solid #2A3139;
                            border-left: 5px solid #1E88E5;
                            border-radius: 12px;
                            padding: 25px;
                            color: #E0E0E0;
                            line-height: 1.8;
                        '>
                            {summary}
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Company information section
            st.markdown('<h3 class="section-header">ℹ️ Company Details</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <p style='color: #9E9E9E; margin: 0; font-size: 0.9em; text-transform: uppercase;'>Industry</p>
                        <p style='color: #43A047; margin: 10px 0 0 0; font-size: 1.3em; font-weight: 600;'>
                            {stock_data.get('industry', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <p style='color: #9E9E9E; margin: 0; font-size: 0.9em; text-transform: uppercase;'>Sector</p>
                        <p style='color: #FB8C00; margin: 10px 0 0 0; font-size: 1.3em; font-weight: 600;'>
                            {stock_data.get('sector', 'N/A')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            description = stock_data.get('description', 'N/A')
            if description and description != 'N/A':
                st.markdown(f"""
                    <div class='metric-card'>
                        <p style='color: #9E9E9E; margin: 0; font-size: 0.9em; text-transform: uppercase;'>About</p>
                        <p style='color: #E0E0E0; margin: 10px 0 0 0; font-size: 1em; line-height: 1.6;'>
                            {description}...
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}", icon="⚠️")

# Sidebar with premium styling
with st.sidebar:
    st.markdown("""
        <h2 style='color: #1E88E5; font-size: 1.5em; margin-bottom: 20px;'>📖 Guide</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='help-text'>
        <h4 style='color: #43A047;'>How to Use:</h4>
        <ol>
            <li>Enter a natural language query about any stock</li>
            <li>Include the company name or ticker symbol</li>
            <li>Optionally specify a time period</li>
        </ol>
        
        <h4 style='color: #43A047; margin-top: 20px;'>Example Queries:</h4>
        <ul>
            <li>"How is Apple stock performing?"</li>
            <li>"Show me Tesla's performance over the past year"</li>
            <li>"Is Microsoft stock strong fundamentally?"</li>
            <li>"Tell me about John Deere stock"</li>
        </ul>
        
        <h4 style='color: #43A047; margin-top: 20px;'>Supported Timeframes:</h4>
        <ul>
            <li><strong>1mo</strong> - Past month</li>
            <li><strong>3mo</strong> - Past 3 months</li>
            <li><strong>6mo</strong> - Past 6 months</li>
            <li><strong>1y</strong> - Past year</li>
            <li><strong>2y</strong> - Past 2 years</li>
            <li><strong>5y</strong> - Past 5 years</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='margin-top: 30px;'>
        <h4 style='color: #1E88E5;'>⚡ Technology Stack</h4>
        <p class='help-text'>
            • <strong>Groq LLM</strong> - AI-powered analysis<br>
            • <strong>yfinance</strong> - Real stock data<br>
            • <strong>Streamlit</strong> - Web interface<br>
            • <strong>Flask</strong> - Backend server
        </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<p style='color: #9E9E9E; text-align: center; margin-top: 40px; font-size: 0.85em;'>Made with ❤️ by FinanceHub</p>", unsafe_allow_html=True)
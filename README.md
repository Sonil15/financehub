# FinanceHub - AI-Powered Financial Analysis Dashboard

> **Intelligent stock analysis using natural language queries and AI-powered insights**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## Overview

FinanceHub is a sophisticated financial analysis platform that combines the power of AI language models with real-time stock market data. Ask questions about any stock in plain English and get comprehensive, data-driven insights powered by Groq's advanced LLM.

### Key Capabilities

- **Natural Language Processing** - Ask about stocks in conversational English
- **AI-Powered Analysis** - Intelligent insights using Groq's LLM (llama-3.3-70b-versatile)
- **Real-Time Data** - Live stock prices, P/E ratios, market caps from Yahoo Finance
- **Historical Analysis** - Automatic detection of timeframes (past month, year, etc.)
- **Beautiful Dashboard** - Modern, responsive Streamlit interface with dark theme
- **Multiple Interfaces** - Web UI, CLI, and programmatic API

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (get it from [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd financial-analysis-mcp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   MCP_SERVER_URL=http://localhost:5001
   ```

### Running the Application

#### Option 1: Web Dashboard (Recommended)

**Terminal 1 - Start the Flask backend:**
```bash
python src/mcp_server.py
```

You should see:
```
 * Running on http://localhost:5001
```

**Terminal 2 - Start the Streamlit frontend:**
```bash
streamlit run src/streamlit_app.py
```

The dashboard will open at `http://localhost:8501`

#### Option 2: Command Line Interface

```bash
python src/ask_finance.py "What is the current price of AAPL?"
python src/ask_finance.py "Show me Apple's P/E ratio and stock history"
```

## 📚 Usage Examples

### Web Dashboard
- Search for any stock ticker
- Ask natural language questions about companies
- View real-time market data and AI-generated insights
- Analyze historical trends and patterns

### Example Queries
```
"What was Apple's stock price 6 months ago?"
"What is the current price of larry ellison's company?"
"Show me Apple's P/E ratio and price history for past month"
"Is Tesla overvalued based on its P/E ratio?"
```

## 🏗️ Project Structure

```
financial-analysis-mcp/
├── src/
│   ├── streamlit_app.py       # Streamlit web dashboard
│   ├── mcp_server.py          # Flask backend server
│   ├── ask_finance.py         # Command-line interface
│   ├── finance_mcp_client.py  # Core analysis engine
│   ├── data_fetchers/         # Folder for data fetchers
│   └── prompts.py             # LLM prompt templates
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |
| `MCP_SERVER_URL` | Backend server URL | Yes |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/ERROR) | No |

## 📦 Dependencies

- **streamlit** - Web UI framework
- **flask** - Backend server
- **yfinance** - Stock market data
- **groq** - AI language model API
- **pandas** - Data manipulation
- **python-dotenv** - Environment variables



# US Stock Market Agent

A Python agent built with Google's Agent Development Kit (ADK) that provides real-time information about top performing stocks in the US market. This agent can retrieve current market movers (top gainers and losers) and provide detailed information about specific stocks.

## Features

- **Top Market Movers**: Get the current day's top gaining and losing stocks
- **Stock Details**: Retrieve comprehensive information about a specific stock
- **Easy Integration**: Built with Google's ADK for seamless integration with conversational AI systems
- **Clean API**: Well-documented functions with clear inputs and outputs

## Prerequisites

- Python 3.8 or higher
- An Alpha Vantage API key (free tier available)
- Google's Agent Development Kit (ADK)

## Installation

1. Clone this repository:
   ```
   git clonehttps://github.com/RashRAJ/stockAIAgent.git
   cd us-stock-market-agent
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install requests python-dotenv google-adk
   ```

4. Create a `.env` file with your Alpha Vantage API key:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```
   You can get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

## Usage

### Basic Usage

```python
from stock_agent import stock_agent

# The agent is ready to use with Google ADK
# stock_agent can be imported directly
```

### Running in ADK Web UI

```bash
# From the parent directory
adk web
```

Then select "stock_market_agent" from the dropdown in the ADK Web UI.

### Example Queries

Once the agent is running, you can ask it questions like:

- "What are today's top market movers?"
- "Show me the biggest stock gainers and losers"
- "Tell me about AAPL stock"
- "What's the current price of Microsoft stock?"

### Using the Functions Directly

You can also use the underlying functions directly in your own code:

```python
from stock_agent import get_market_movers, get_stock_details

# Get top 5 gainers and losers
movers = get_market_movers(limit=5)
if movers["status"] == "success":
    print(movers["report"])
    
    # Access the raw data
    top_gainers = movers["gainers"]
    top_losers = movers["losers"]

# Get details about a specific stock
apple = get_stock_details("AAPL")
if apple["status"] == "success":
    print(apple["report"])
    
    # Access specific data points
    price = apple["price"]
    change_percent = apple["change_percent"]
    sector = apple["sector"]
```

## Function Documentation

### `get_market_movers(limit=10)`

Retrieves the top gainers and losers from the US stock market at the current time.

**Parameters:**
- `limit` (int): Number of stocks to return for each category (gainers/losers)

**Returns:**
- `dict`: Contains status and lists of top gainers and losers with their performance data

### `get_stock_details(symbol)`

Retrieves detailed information for a specific stock.

**Parameters:**
- `symbol` (str): The stock symbol to lookup (e.g., 'AAPL', 'MSFT')

**Returns:**
- `dict`: Status and detailed information about the stock

## Project Structure

```
us-stock-market-agent/
├── __init__.py
├── stock_agent.py     # Main agent implementation
├── .env               # Environment variables (API keys)
└── README.md          # This file
```

## API Rate Limits

The free tier of Alpha Vantage has the following limitations:
- 5 API requests per minute
- 500 requests per day

For higher limits, consider upgrading to a paid plan.

## Alternatives

If you prefer using the Polygon.io API instead of Alpha Vantage, there's an alternative implementation available in the `polygon_implementation` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Google Agent Development Kit](https://github.com/google-ai/agent-development-kit) for providing the agent framework
- [Alpha Vantage](https://www.alphavantage.co/) for providing the market data API
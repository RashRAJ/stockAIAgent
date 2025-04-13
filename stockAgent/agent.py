"""
Stock Market Agent with Alpha Vantage API

This module defines a stock market agent that retrieves information about 
top gainers and losers in the US market and gets details about specific stocks
using the Alpha Vantage API, which is an alternative to Polygon.io.
"""

import os
import datetime
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

# Get API key from environment
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")

def get_market_movers(limit: int = 10) -> Dict[str, Any]:
    """Retrieves the top gainers and losers from the US stock market at the current time.

    Args:
        limit (int): Number of stocks to return for each category (gainers/losers).

    Returns:
        dict: Contains status and lists of top gainers and losers with their performance data.
    """
    try:
        # Call Alpha Vantage API for top gainers
        gainers_url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(gainers_url)
        
        if response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"API request failed with status code {response.status_code}"
            }
            
        data = response.json()
        
        # Process top gainers
        gainers = []
        if "top_gainers" in data:
            for stock in data["top_gainers"][:limit]:
                gainers.append({
                    "symbol": stock.get("ticker", ""),
                    "name": stock.get("name", ""),
                    "price": float(stock.get("price", "0").replace("$", "")),
                    "change": float(stock.get("change_amount", "0").replace("$", "")),
                    "change_percent": float(stock.get("change_percentage", "0%").replace("%", "")),
                    "volume": int(stock.get("volume", "0").replace(",", ""))
                })
                
        # Process top losers
        losers = []
        if "top_losers" in data:
            for stock in data["top_losers"][:limit]:
                losers.append({
                    "symbol": stock.get("ticker", ""),
                    "name": stock.get("name", ""),
                    "price": float(stock.get("price", "0").replace("$", "")),
                    "change": float(stock.get("change_amount", "0").replace("$", "")),
                    "change_percent": float(stock.get("change_percentage", "0%").replace("%", "")),
                    "volume": int(stock.get("volume", "0").replace(",", ""))
                })
                
        # Format the response
        gainers_report = "Top Gainers:\n"
        for idx, stock in enumerate(gainers, 1):
            gainers_report += f"{idx}. {stock['symbol']} ({stock['name']}): +{stock['change_percent']}%, ${stock['price']}\n"
            
        losers_report = "\nTop Losers:\n"
        for idx, stock in enumerate(losers, 1):
            losers_report += f"{idx}. {stock['symbol']} ({stock['name']}): {stock['change_percent']}%, ${stock['price']}\n"
            
        full_report = gainers_report + losers_report
        
        return {
            "status": "success",
            "report": full_report,
            "gainers": gainers,
            "losers": losers,
            "last_updated": data.get("last_updated", "Unknown")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve market movers: {str(e)}"
        }

def get_stock_details(symbol: str) -> Dict[str, Any]:
    """Retrieves detailed information for a specific stock.

    Args:
        symbol (str): The stock symbol to lookup (e.g., 'AAPL', 'MSFT')

    Returns:
        dict: Status and detailed information about the stock
    """
    try:
        # Get overview data
        overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        overview_response = requests.get(overview_url)
        
        if overview_response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"API request failed with status code {overview_response.status_code}"
            }
            
        overview_data = overview_response.json()
        
        # Check if we got valid data
        if "Symbol" not in overview_data:
            return {
                "status": "error",
                "error_message": f"No data found for symbol {symbol}"
            }
            
        # Get quote data
        quote_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        quote_response = requests.get(quote_url)
        
        if quote_response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"API request failed with status code {quote_response.status_code}"
            }
            
        quote_data = quote_response.json().get("Global Quote", {})
        
        # Extract and format data
        price = float(quote_data.get("05. price", "0"))
        prev_close = float(quote_data.get("08. previous close", "0"))
        change = float(quote_data.get("09. change", "0"))
        change_percent = float(quote_data.get("10. change percent", "0%").replace("%", ""))
        
        # Format the report
        report = f"Stock Details for {symbol} ({overview_data.get('Name', symbol)}):\n"
        report += f"Price: ${price}\n"
        report += f"Change: {'+' if change >= 0 else ''}{change} ({'+' if change_percent >= 0 else ''}{change_percent}%)\n"
        report += f"Sector: {overview_data.get('Sector', 'Unknown')}\n"
        report += f"Industry: {overview_data.get('Industry', 'Unknown')}\n"
        report += f"Market Cap: ${float(overview_data.get('MarketCapitalization', '0')) / 1e9:.2f} billion\n"
        report += f"P/E Ratio: {overview_data.get('PERatio', 'N/A')}\n"
        report += f"Dividend Yield: {overview_data.get('DividendYield', 'N/A')}\n"
        report += f"52-week High: ${overview_data.get('52WeekHigh', 'N/A')}\n"
        report += f"52-week Low: ${overview_data.get('52WeekLow', 'N/A')}\n"
        report += f"Volume: {int(quote_data.get('06. volume', '0')):,}\n"
        
        return {
            "status": "success",
            "report": report,
            "symbol": symbol,
            "name": overview_data.get('Name', symbol),
            "price": price,
            "change": change,
            "change_percent": change_percent,
            "sector": overview_data.get('Sector', 'Unknown'),
            "industry": overview_data.get('Industry', 'Unknown'),
            "description": overview_data.get('Description', '')
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to retrieve stock details for {symbol}: {str(e)}"
        }

# Create the agent
root_agent = Agent(
    name="stock_market_agent",
    model="gemini-2.0-flash",  # Or your preferred model
    description=(
        "Agent to provide information about US stock market performance"
    ),
    instruction=(
        "You are a helpful financial agent who can answer user questions about the "
        "stock market, retrieve information about top gainers and losers, and "
        "provide details about specific stocks. with extra information and contex about the company what you should look for in the stock market. weather you should invest in them or not including sources for extra information on the stock current CEO and latest information about the company and economic laws affect the stock market."
    ),
    tools=[get_market_movers, get_stock_details],
)


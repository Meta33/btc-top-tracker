#!/usr/bin/env python3
"""
Fetch live market data from various APIs
"""
import requests
import json
import os
from datetime import datetime, timedelta
import yfinance as yf

def fetch_coingecko_data():
    """Fetch BTC price, dominance, and TOTAL2 from CoinGecko (FREE)"""
    try:
        # BTC price and dominance
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        btc_data = response.json()["bitcoin"]
        
        # Global market data for dominance
        global_url = "https://api.coingecko.com/api/v3/global"
        global_response = requests.get(global_url, timeout=10)
        global_data = global_response.json()["data"]
        
        return {
            "btc_price": btc_data["usd"],
            "btc_dominance": global_data["market_cap_percentage"]["btc"],
            "total_market_cap": global_data["total_market_cap"]["usd"],
            "total2": global_data["total_market_cap"]["usd"] - (btc_data["market_cap"]),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"❌ CoinGecko fetch failed: {e}")
        return None

def fetch_spx_data():
    """Fetch S&P 500 data from Yahoo Finance (FREE)"""
    try:
        spx = yf.Ticker("^GSPC")
        hist = spx.history(period="1mo")
        current_price = hist['Close'].iloc[-1]
        
        # Get 50-day and 200-day MA
        hist_long = spx.history(period="1y")
        ma_50 = hist_long['Close'].tail(50).mean()
        ma_200 = hist_long['Close'].tail(200).mean()
        
        return {
            "spx_price": float(current_price),
            "spx_ma50": float(ma_50),
            "spx_ma200": float(ma_200),
            "death_cross": ma_50 < ma_200
        }
    except Exception as e:
        print(f"❌ SPX fetch failed: {e}")
        return None

def fetch_btc_ma():
    """Calculate BTC moving averages"""
    try:
        btc = yf.Ticker("BTC-USD")
        hist = spx.history(period="1y")
        
        ma_50 = hist['Close'].tail(50).mean()
        ma_200 = hist['Close'].tail(200).mean()
        
        return {
            "btc_ma50": float(ma_50),
            "btc_ma200": float(ma_200),
            "btc_death_cross": ma_50 < ma_200
        }
    except Exception as e:
        print(f"❌ BTC MA calculation failed: {e}")
        return None

def fetch_m2_data():
    """Fetch M2 money supply from FRED (FREE, no API key needed)"""
    try:
        # Use FRED's public CSV endpoint
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        params = {
            "id": "M2SL",
            "cosd": (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d"),
            "coed": datetime.now().strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params, timeout=10)
        
        # Parse CSV
        lines = response.text.strip().split('\n')
        latest = lines[-1].split(',')
        previous_year = lines[-365].split(',') if len(lines) > 365 else lines[0].split(',')
        
        latest_value = float(latest[1])
        prev_value = float(previous_year[1])
        yoy_growth = ((latest_value - prev_value) / prev_value) * 100
        
        return {
            "m2_current": latest_value,
            "m2_yoy_growth": yoy_growth,
            "m2_negative": yoy_growth < 0
        }
    except Exception as e:
        print(f"❌ M2 fetch failed: {e}")
        return None

def fetch_lth_data():
    """Fetch LTH distribution data (requires Glassnode API key)"""
    api_key = os.getenv('GLASSNODE_API_KEY')
    
    if not api_key:
        print("⚠️  No Glassnode API key - using placeholder")
        return {"lth_distribution": 0, "lth_elevated": False}
    
    try:
        url = "https://api.glassnode.com/v1/metrics/supply/lth_sum"
        params = {
            "a": "BTC",
            "api_key": api_key,
            "s": int((datetime.now() - timedelta(days=30)).timestamp()),
            "u": int(datetime.now().timestamp())
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # Calculate 7-day moving average of change
        if len(data) >= 7:
            recent_change = (data[-1]['v'] - data[-7]['v']) / 7
            return {
                "lth_distribution": recent_change,
                "lth_elevated": recent_change < -50000  # More than 50k BTC/day selling
            }
        return {"lth_distribution": 0, "lth_elevated": False}
    except Exception as e:
        print(f"❌ LTH fetch failed: {e}")
        return {"lth_distribution": 0, "lth_elevated": False}

def main():
    """Main fetch function"""
    print("🔍 Fetching market data...")
    
    # Fetch all data sources
    cg_data = fetch_coingecko_data()
    spx_data = fetch_spx_data()
    btc_ma = fetch_btc_ma()
    m2_data = fetch_m2_data()
    lth_data = fetch_lth_data()
    
    # Combine all data
    combined_data = {
        "timestamp": datetime.utcnow().isoformat(),
        **( cg_data or {}),
        **(spx_data or {}),
        **(btc_ma or {}),
        **(m2_data or {}),
        **(lth_data or {})
    }
    
    # Save to JSON
    os.makedirs('data', exist_ok=True)
    with open('data/latest_data.json', 'w') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"✅ Data fetched: BTC ${combined_data.get('btc_price', 'N/A'):,.0f}, SPX {combined_data.get('spx_price', 'N/A'):,.0f}")
    return combined_data

if __name__ == "__main__":
    main()

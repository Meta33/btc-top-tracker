#!/usr/bin/env python3
"""
Fetch live market data from various APIs
"""

import requests
import json
import os
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not available - using CoinGecko only")

def fetch_coingecko_data():
    """Fetch BTC price, dominance, and TOTAL2 from CoinGecko (FREE)"""
    try:
        # BTC price and market cap
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24h_vol": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        btc_data = response.json()["bitcoin"]
        
        # Global market data for dominance
        global_url = "https://api.coingecko.com/api/v3/global"
        global_response = requests.get(global_url, timeout=10)
        global_data = global_response.json()["data"]
        
        # Calculate USDT dominance (approximate from stablecoins)
        usdt_url = "https://api.coingecko.com/api/v3/simple/price"
        usdt_params = {
            "ids": "tether",
            "vs_currencies": "usd",
            "include_market_cap": "true"
        }
        usdt_response = requests.get(usdt_url, params=usdt_params, timeout=10)
        usdt_market_cap = usdt_response.json()["tether"]["usd_market_cap"]
        
        total_market_cap = global_data["total_market_cap"]["usd"]
        btc_dominance = global_data["market_cap_percentage"]["bitcoin"]
        usdt_dominance = (usdt_market_cap / total_market_cap) * 100
        
        # TOTAL2 = Total market cap - BTC market cap
        total2 = total_market_cap - btc_data["usd_market_cap"]
        
        return {
            "btc_price": btc_data["usd"],
            "btc_dominance": btc_dominance,
            "usdt_dominance": usdt_dominance,
            "total2": total2,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"❌ CoinGecko fetch failed: {e}")
        return None

def fetch_spx_data():
    """Fetch S&P 500 data from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        return {"spx_price": None, "spx_rollover": None}
    
    try:
        spx = yf.Ticker("^GSPC")
        hist = spx.history(period="200d")
        
        if len(hist) == 0:
            raise ValueError("No SPX data returned")
        
        current_price = hist['Close'].iloc[-1]
        ma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
        spx_rollover = current_price < ma200
        
        return {
            "spx_price": float(current_price),
            "spx_rollover": bool(spx_rollover)
        }
    except Exception as e:
        print(f"❌ SPX fetch failed: {e}")
        return {"spx_price": None, "spx_rollover": None}

def fetch_m2_data():
    """Fetch M2 money supply from FRED"""
    try:
        # FRED API - M2SL (M2 Money Stock)
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": "WM2NS",  # Weekly M2 (more current than monthly M2SL)
            "api_key": "YOUR_FRED_API_KEY",  # Public data, key optional
            "file_type": "json",
            "sort_order": "desc",
            "limit": "52"  # Last year of weekly data
        }
        
        # Try without API key first (public data)
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get("observations", [])
            
            if len(observations) >= 2:
                latest_value = float(observations[0]["value"])
                year_ago_value = float(observations[-1]["value"])
                m2_growth = ((latest_value - year_ago_value) / year_ago_value) * 100
                
                return {
                    "m2_growth": m2_growth,
                    "m2_slowing": m2_growth < 5.0  # Below 5% YoY = slowing
                }
        
        # Fallback: use placeholder
        print("⚠️ M2 fetch failed - using placeholder")
        return {"m2_growth": None, "m2_slowing": None}
        
    except Exception as e:
        print(f"❌ M2 fetch failed: {e}")
        return {"m2_growth": None, "m2_slowing": None}

def fetch_lth_data():
    """Fetch Long-Term Holder distribution (Glassnode)"""
    glassnode_key = os.environ.get("GLASSNODE_API_KEY")
    
    if not glassnode_key:
        print("⚠️ No Glassnode API key - using placeholder")
        return {"lth_distribution": None, "lth_elevated": None}
    
    try:
        url = "https://api.glassnode.com/v1/metrics/distribution/balance_1y_hodl_waves"
        params = {
            "a": "BTC",
            "api_key": glassnode_key,
            "s": int((datetime.utcnow() - timedelta(days=90)).timestamp()),
            "u": int(datetime.utcnow().timestamp())
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if len(data) > 0:
            current_lth = data[-1]["v"]
            baseline_lth = sum([d["v"] for d in data[:30]]) / 30
            lth_elevated = current_lth > (baseline_lth * 3)
            
            return {
                "lth_distribution": current_lth,
                "lth_elevated": lth_elevated
            }
    except Exception as e:
        print(f"❌ LTH fetch failed: {e}")
    
    return {"lth_distribution": None, "lth_elevated": None}

def main():
    print("🔄 Fetching market data...")
    
    # Combine all data sources
    combined_data = {}
    
    # CoinGecko (required)
    coingecko = fetch_coingecko_data()
    if coingecko:
        combined_data.update(coingecko)
    else:
        print("❌ Critical: CoinGecko data unavailable")
        exit(1)
    
    # SPX (optional but recommended)
    spx_data = fetch_spx_data()
    combined_data.update(spx_data)
    
    # M2 (optional)
    m2_data = fetch_m2_data()
    combined_data.update(m2_data)
    
    # LTH (optional, requires API key)
    lth_data = fetch_lth_data()
    combined_data.update(lth_data)
    
    # Save to file
    output_path = "data/latest_data.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"✅ Data saved to {output_path}")
    print(f"   BTC: ${combined_data.get('btc_price', 'N/A'):,.0f}")
    print(f"   BTC Dominance: {combined_data.get('btc_dominance', 'N/A'):.1f}%")
    print(f"   USDT Dominance: {combined_data.get('usdt_dominance', 'N/A'):.1f}%")

if __name__ == "__main__":
    main()

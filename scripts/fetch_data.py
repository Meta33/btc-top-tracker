#!/usr/bin/env python3
"""
Fetch live market data from various APIs
ROBUST VERSION - Better error handling and headers
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not available - SPX/BTC data will be unavailable")

# User-Agent to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json'
}

def fetch_coingecko_data():
    """Fetch BTC price, dominance, and TOTAL2 from CoinGecko (FREE)"""
    try:
        print("🔄 Fetching CoinGecko data...")
        
        # BTC price and market cap
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,tether",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24h_vol": "true"
        }
        
        print(f"   Requesting: {url}")
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   Response text: {response.text[:200]}")
            raise Exception(f"HTTP {response.status_code}")
        
        price_data = response.json()
        print(f"   Response keys: {list(price_data.keys())}")
        
        if "bitcoin" not in price_data:
            print(f"   Full response: {json.dumps(price_data, indent=2)}")
            raise Exception("'bitcoin' key not in response")
        
        btc_price = price_data["bitcoin"]["usd"]
        btc_market_cap = price_data["bitcoin"]["usd_market_cap"]
        
        # Add small delay to avoid rate limiting
        time.sleep(1)
        
        # Tether data
        if "tether" in price_data:
            usdt_market_cap = price_data["tether"]["usd_market_cap"]
        else:
            print("   ⚠️ Tether data not available, using placeholder")
            usdt_market_cap = 120000000000  # ~$120B placeholder
        
        # Add small delay
        time.sleep(1)
        
        # Global market data for dominance
        print("   Fetching global market data...")
        global_url = "https://api.coingecko.com/api/v3/global"
        global_response = requests.get(global_url, headers=HEADERS, timeout=15)
        global_response.raise_for_status()
        global_data = global_response.json()["data"]
        
        total_market_cap = global_data["total_market_cap"]["usd"]
        btc_dominance = global_data["market_cap_percentage"]["btc"]
        usdt_dominance = (usdt_market_cap / total_market_cap) * 100
        
        # TOTAL2 = Total market cap - BTC market cap
        total2 = total_market_cap - btc_market_cap
        
        print(f"✅ CoinGecko data fetched successfully")
        print(f"   BTC: ${btc_price:,.0f}")
        print(f"   BTC Dominance: {btc_dominance:.1f}%")
        print(f"   USDT Dominance: {usdt_dominance:.1f}%")
        
        return {
            "btc_price": btc_price,
            "btc_dominance": btc_dominance,
            "usdt_dominance": usdt_dominance,
            "total2": total2,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"❌ CoinGecko fetch failed: {e}")
        print(f"   Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

def fetch_spx_data():
    """Fetch S&P 500 data from Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        print("⚠️ yfinance not available - SPX data unavailable")
        return {"spx_price": None, "spx_rollover": None}
    
    try:
        print("🔄 Fetching SPX data...")
        spx = yf.Ticker("^GSPC")
        hist = spx.history(period="200d")
        
        if len(hist) == 0:
            raise ValueError("No SPX data returned")
        
        current_price = hist['Close'].iloc[-1]
        
        # Calculate 200-day MA
        if len(hist) >= 200:
            ma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            spx_rollover = current_price < ma200
        else:
            # Not enough data for full 200-day MA
            ma200 = hist['Close'].mean()
            spx_rollover = False
        
        print(f"✅ SPX data fetched: ${current_price:,.0f} (MA200: ${ma200:,.0f})")
        
        return {
            "spx_price": float(current_price),
            "spx_rollover": bool(spx_rollover)
        }
    except Exception as e:
        print(f"❌ SPX fetch failed: {e}")
        return {"spx_price": None, "spx_rollover": None}

def fetch_m2_data():
    """Fetch M2 money supply from FRED (uses public data, no API key needed)"""
    try:
        # Note: FRED may require API key for frequent requests
        # For now, use placeholder since API access is limited
        print("⚠️ M2 data requires FRED API key - using placeholder")
        return {"m2_growth": None, "m2_slowing": None}
        
    except Exception as e:
        print(f"❌ M2 fetch failed: {e}")
        return {"m2_growth": None, "m2_slowing": None}

def fetch_lth_data():
    """Fetch Long-Term Holder distribution (Glassnode)"""
    glassnode_key = os.environ.get("GLASSNODE_API_KEY")
    
    if not glassnode_key:
        print("⚠️ No Glassnode API key - LTH data unavailable")
        return {"lth_distribution": None, "lth_elevated": None}
    
    try:
        print("🔄 Fetching LTH data...")
        url = "https://api.glassnode.com/v1/metrics/distribution/balance_1y_hodl_waves"
        params = {
            "a": "BTC",
            "api_key": glassnode_key,
            "s": int((datetime.now() - timedelta(days=90)).timestamp()),
            "u": int(datetime.now().timestamp())
        }
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if len(data) > 0:
            current_lth = data[-1]["v"]
            baseline_lth = sum([d["v"] for d in data[:30]]) / 30
            lth_elevated = current_lth > (baseline_lth * 3)
            
            print(f"✅ LTH data fetched: {current_lth} BTC/day")
            
            return {
                "lth_distribution": current_lth,
                "lth_elevated": lth_elevated
            }
    except Exception as e:
        print(f"❌ LTH fetch failed: {e}")
    
    return {"lth_distribution": None, "lth_elevated": None}

def main():
    print("🔄 Fetching market data...")
    print()
    
    # Combine all data sources
    combined_data = {}
    
    # CoinGecko (required)
    coingecko = fetch_coingecko_data()
    if coingecko:
        combined_data.update(coingecko)
    else:
        print("❌ CRITICAL: CoinGecko data unavailable")
        exit(1)
    
    print()
    
    # SPX (optional but recommended)
    spx_data = fetch_spx_data()
    combined_data.update(spx_data)
    
    print()
    
    # M2 (optional)
    m2_data = fetch_m2_data()
    combined_data.update(m2_data)
    
    print()
    
    # LTH (optional, requires API key)
    lth_data = fetch_lth_data()
    combined_data.update(lth_data)
    
    print()
    
    # Save to file
    output_path = "data/latest_data.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"✅ Data saved to {output_path}")
    print()
    print("📊 Summary:")
    print(f"   BTC Price: ${combined_data.get('btc_price', 'N/A'):,.0f}")
    print(f"   BTC Dominance: {combined_data.get('btc_dominance', 'N/A'):.1f}%")
    print(f"   USDT Dominance: {combined_data.get('usdt_dominance', 'N/A'):.1f}%")
    print(f"   SPX Price: ${combined_data.get('spx_price', 'N/A'):,.0f}" if combined_data.get('spx_price') else "   SPX Price: N/A")

if __name__ == "__main__":
    main()

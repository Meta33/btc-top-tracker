#!/usr/bin/env python3
"""
FREE Smart Money Tracker - No Paid APIs Required
Uses: Blockchain.com (FREE), CoinGecko (FREE), Yahoo Finance (FREE)
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta
from statistics import mean

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance not available")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json'
}

def fetch_coingecko_data():
    """Fetch BTC price, dominance from CoinGecko (FREE)"""
    try:
        print("🔄 Fetching CoinGecko data...")
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,tether",
            "vs_currencies": "usd",
            "include_market_cap": "true"
        }
        
        response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
        price_data = response.json()
        
        btc_price = price_data["bitcoin"]["usd"]
        btc_market_cap = price_data["bitcoin"]["usd_market_cap"]
        usdt_market_cap = price_data.get("tether", {}).get("usd_market_cap", 120000000000)
        
        time.sleep(1)
        
        # Global data
        global_url = "https://api.coingecko.com/api/v3/global"
        global_response = requests.get(global_url, headers=HEADERS, timeout=15)
        global_response.raise_for_status()
        global_data = global_response.json()["data"]
        
        total_market_cap = global_data["total_market_cap"]["usd"]
        btc_dominance = global_data["market_cap_percentage"]["btc"]
        usdt_dominance = (usdt_market_cap / total_market_cap) * 100
        total2 = total_market_cap - btc_market_cap
        
        print(f"✅ CoinGecko: BTC ${btc_price:,.0f} | Dom {btc_dominance:.1f}%")
        
        return {
            "btc_price": btc_price,
            "btc_dominance": btc_dominance,
            "usdt_dominance": usdt_dominance,
            "total2": total2
        }
    except Exception as e:
        print(f"❌ CoinGecko failed: {e}")
        return None

def fetch_blockchain_smart_money():
    """Fetch FREE smart money proxies from Blockchain.com"""
    try:
        print("🔄 Fetching FREE smart money data (Blockchain.com)...")
        
        results = {}
        
        # 1. Trade Volume (proxy for institutional activity)
        print("   📊 Trade Volume...")
        vol_url = "https://api.blockchain.info/charts/trade-volume"
        vol_params = {"timespan": "90days", "format": "json", "sampled": "false"}
        vol_response = requests.get(vol_url, params=vol_params, timeout=15)
        
        if vol_response.status_code == 200:
            vol_data = vol_response.json()
            if vol_data.get("values") and len(vol_data["values"]) > 0:
                recent_vol = [v["y"] for v in vol_data["values"][-7:]]  # Last 7 days
                baseline_vol = [v["y"] for v in vol_data["values"][-30:-7]]  # Previous 23 days
                
                current_vol = mean(recent_vol)
                baseline_vol_avg = mean(baseline_vol) if baseline_vol else current_vol
                
                vol_spike = current_vol > (baseline_vol_avg * 1.5)  # 50% above baseline
                
                results["trade_volume"] = {
                    "current": current_vol,
                    "baseline": baseline_vol_avg,
                    "spike": vol_spike
                }
                print(f"      ✅ Current: ${current_vol/1e9:.2f}B | Baseline: ${baseline_vol_avg/1e9:.2f}B")
        
        time.sleep(1)
        
        # 2. Transaction Count (network activity)
        print("   📈 Transaction Count...")
        tx_url = "https://api.blockchain.info/charts/n-transactions"
        tx_params = {"timespan": "90days", "format": "json", "sampled": "false"}
        tx_response = requests.get(tx_url, params=tx_params, timeout=15)
        
        if tx_response.status_code == 200:
            tx_data = tx_response.json()
            if tx_data.get("values") and len(tx_data["values"]) > 0:
                recent_tx = [v["y"] for v in tx_data["values"][-7:]]
                baseline_tx = [v["y"] for v in tx_data["values"][-30:-7]]
                
                current_tx = mean(recent_tx)
                baseline_tx_avg = mean(baseline_tx) if baseline_tx else current_tx
                
                tx_elevated = current_tx > (baseline_tx_avg * 1.3)
                
                results["transaction_count"] = {
                    "current": current_tx,
                    "baseline": baseline_tx_avg,
                    "elevated": tx_elevated
                }
                print(f"      ✅ Current: {current_tx:,.0f}/day | Baseline: {baseline_tx_avg:,.0f}/day")
        
        time.sleep(1)
        
        # 3. Market Cap Changes (smart money entering/exiting)
        print("   💰 Market Cap Trend...")
        cap_url = "https://api.blockchain.info/charts/market-cap"
        cap_params = {"timespan": "90days", "format": "json", "sampled": "false"}
        cap_response = requests.get(cap_url, params=cap_params, timeout=15)
        
        if cap_response.status_code == 200:
            cap_data = cap_response.json()
            if cap_data.get("values") and len(cap_data["values"]) > 30:
                recent_cap = cap_data["values"][-1]["y"]
                month_ago_cap = cap_data["values"][-30]["y"]
                
                cap_change_pct = ((recent_cap - month_ago_cap) / month_ago_cap) * 100
                cap_declining = cap_change_pct < -5  # Down more than 5%
                
                results["market_cap_trend"] = {
                    "current": recent_cap,
                    "month_ago": month_ago_cap,
                    "change_pct": cap_change_pct,
                    "declining": cap_declining
                }
                print(f"      ✅ 30-day change: {cap_change_pct:+.1f}%")
        
        time.sleep(1)
        
        # 4. Hash Rate (miner confidence)
        print("   ⛏️  Hash Rate...")
        hash_url = "https://api.blockchain.info/charts/hash-rate"
        hash_params = {"timespan": "90days", "format": "json", "sampled": "false"}
        hash_response = requests.get(hash_url, params=hash_params, timeout=15)
        
        if hash_response.status_code == 200:
            hash_data = hash_response.json()
            if hash_data.get("values") and len(hash_data["values"]) > 30:
                recent_hash = hash_data["values"][-1]["y"]
                month_ago_hash = hash_data["values"][-30]["y"]
                
                hash_change_pct = ((recent_hash - month_ago_hash) / month_ago_hash) * 100
                hash_declining = hash_change_pct < -10  # Down more than 10%
                
                results["hash_rate_trend"] = {
                    "current": recent_hash,
                    "change_pct": hash_change_pct,
                    "declining": hash_declining
                }
                print(f"      ✅ 30-day change: {hash_change_pct:+.1f}%")
        
        # 5. Exchange Trade Volume Spike Detection
        print("   🚨 Volume Spike Analysis...")
        if results.get("trade_volume"):
            vol_spike_detected = results["trade_volume"]["spike"]
            results["volume_spike_alert"] = vol_spike_detected
            print(f"      {'🔴 SPIKE DETECTED' if vol_spike_detected else '🟢 Normal'}")
        
        print(f"✅ FREE Smart Money Data: {len(results)} metrics fetched")
        
        return results
        
    except Exception as e:
        print(f"❌ Blockchain.com failed: {e}")
        import traceback
        traceback.print_exc()
        return {}

def fetch_spx_data():
    """Fetch S&P 500 data"""
    if not YFINANCE_AVAILABLE:
        return {"spx_price": None, "spx_rollover": None}
    
    try:
        print("🔄 Fetching SPX data...")
        spx = yf.Ticker("^GSPC")
        hist = spx.history(period="200d")
        
        if len(hist) == 0:
            return {"spx_price": None, "spx_rollover": None}
        
        current_price = hist['Close'].iloc[-1]
        
        if len(hist) >= 200:
            ma200 = hist['Close'].rolling(window=200).mean().iloc[-1]
            spx_rollover = current_price < ma200
        else:
            spx_rollover = False
        
        print(f"✅ SPX: ${current_price:,.0f}")
        
        return {
            "spx_price": float(current_price),
            "spx_rollover": bool(spx_rollover)
        }
    except Exception as e:
        print(f"❌ SPX failed: {e}")
        return {"spx_price": None, "spx_rollover": None}

def main():
    print("=" * 70)
    print("🆓 FREE SMART MONEY TRACKER - Data Fetch")
    print("=" * 70)
    print()
    
    combined_data = {"timestamp": datetime.now().isoformat()}
    
    # CoinGecko (required)
    print("1️⃣ COINGECKO DATA")
    print("-" * 70)
    coingecko = fetch_coingecko_data()
    if coingecko:
        combined_data.update(coingecko)
    else:
        print("❌ CRITICAL: CoinGecko unavailable")
        exit(1)
    
    print()
    
    # Blockchain.com Smart Money (FREE)
    print("2️⃣ BLOCKCHAIN.COM SMART MONEY DATA (FREE)")
    print("-" * 70)
    blockchain_data = fetch_blockchain_smart_money()
    combined_data.update(blockchain_data)
    
    print()
    
    # SPX
    print("3️⃣ SPX MARKET DATA")
    print("-" * 70)
    spx_data = fetch_spx_data()
    combined_data.update(spx_data)
    
    print()
    print("=" * 70)
    
    # Save
    output_path = "data/latest_data.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"✅ Data saved to {output_path}")
    print()
    print("📊 SUMMARY:")
    print(f"   BTC Price: ${combined_data.get('btc_price', 'N/A'):,.0f}")
    print(f"   BTC Dominance: {combined_data.get('btc_dominance', 'N/A'):.1f}%")
    print(f"   Smart Money Tracking: ✅ FREE EDITION")
    print(f"   Volume Spike: {'🔴 YES' if combined_data.get('volume_spike_alert') else '🟢 NO'}")
    print("=" * 70)

if __name__ == "__main__":
    main()

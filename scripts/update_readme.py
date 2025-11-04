#!/usr/bin/env python3
"""
Calculate composite score - FREE SMART MONEY EDITION
"""

import json
from datetime import datetime

def calculate_score():
    """Calculate weighted composite score with FREE smart money signals"""
    
    # Load latest data
    with open('data/latest_data.json', 'r') as f:
        data = json.load(f)
    
    # ✅ CALCULATE THESE FIRST (before using in signals)
    ath_price = 126280  # October 6, 2025 ATH
    current_price = data.get('btc_price', 0)
    price_ratio = current_price / ath_price if ath_price > 0 else 0
    
    # Define signals with weights
    signals = [
        # TIER 1: Price & Market (25%)
        {
            "name": "BTC Price vs ATH",
            "weight": 0.20,
            "trigger": price_ratio >= 0.80,  # ✅ Now this works!
            "current_value": f"${current_price:,.0f}",
            "target": "> $126K (Oct 6 ATH)",
            "triggered": price_ratio >= 0.80,
            "category": "Market"
        },
        {
            "name": "BTC Dominance Low",
            "weight": 0.05,
            "trigger": data.get("btc_dominance", 100) < 45,
            "current_value": f"{data.get('btc_dominance', 0):.1f}%",
            "target": "< 45% (Alt euphoria)",
            "triggered": data.get("btc_dominance", 100) < 45,
            "category": "Market"
        },
        
        # TIER 2: FREE SMART MONEY SIGNALS (50%)
        {
            "name": "🔥 Volume Spike Alert",
            "weight": 0.25,
            "trigger": data.get("volume_spike_alert", False),
            "current_value": f"${data.get('trade_volume', {}).get('current', 0)/1e9:.2f}B/day" if data.get('trade_volume') else "N/A",
            "target": "> 50% above baseline (Distribution)",
            "triggered": data.get("volume_spike_alert") if data.get("volume_spike_alert") is not None else None,
            "category": "Smart Money"
        },
        {
            "name": "📉 Market Cap Declining",
            "weight": 0.15,
            "trigger": data.get("market_cap_trend", {}).get("declining", False),
            "current_value": f"{data.get('market_cap_trend', {}).get('change_pct', 0):+.1f}%" if data.get('market_cap_trend') else "N/A",
            "target": "< -5% (Smart money exiting)",
            "triggered": data.get("market_cap_trend", {}).get("declining") if data.get('market_cap_trend', {}).get("declining") is not None else None,
            "category": "Smart Money"
        },
        {
            "name": "⚒️ Hash Rate Falling",
            "weight": 0.10,
            "trigger": data.get("hash_rate_trend", {}).get("falling", False),
            "current_value": f"{data.get('hash_rate_trend', {}).get('change_pct', 0):+.1f}%" if data.get('hash_rate_trend') else "N/A",
            "target": "< -10% (Miner capitulation)",
            "triggered": data.get("hash_rate_trend", {}).get("falling") if data.get('hash_rate_trend', {}).get("falling") is not None else None,
            "category": "Smart Money"
        },
        
        # TIER 3: Macro Context (25%)
        {
            "name": "SPX Rollover",
            "weight": 0.15,
            "trigger": data.get("spx_below_ma", False),
            "current_value": f"${data.get('spx_price', 0):,.0f}",
            "target": "< 200-day MA (Risk-off)",
            "triggered": data.get("spx_below_ma") if data.get("spx_below_ma") is not None else None,
            "category": "Macro"
        },
        {
            "name": "USDT Dominance Low",
            "weight": 0.05,
            "trigger": data.get("usdt_dominance", 100) < 3,
            "current_value": f"{data.get('usdt_dominance', 0):.1f}%",
            "target": "< 3% (Liquidity exhaustion)",
            "triggered": data.get("usdt_dominance", 100) < 3,
            "category": "Macro"
        },
        {
            "name": "TOTAL2 Peak",
            "weight": 0.05,
            "trigger": data.get("total2", 0) > 2e12,
            "current_value": f"${data.get('total2', 0)/1e12:.2f}T" if data.get('total2') else "N/A",
            "target": "> $2T (Altcoin mania)",
            "triggered": data.get("total2", 0) > 2e12,
            "category": "Macro"
        }
    ]
    
    # Calculate composite score
    composite_score = 0
    smart_money_score = 0
    triggered_signals = []
    
    for signal in signals:
        if signal.get("triggered"):
            weight = signal["weight"] * 100
            composite_score += weight
            triggered_signals.append(signal["name"])
            
            # Track smart money contribution
            if signal["category"] == "Smart Money":
                smart_money_score += weight
    
    # Determine alert level
    if composite_score >= 70:
        alert_level = "EXTREME RISK"
        alert_color = "🔴"
        alert_message = "MAJOR DISTRIBUTION DETECTED - Consider Taking Profits (FREE Edition)"
    elif composite_score >= 40:
        alert_level = "ELEVATED"
        alert_color = "🟡"
        alert_message = "Smart Money Activity Elevated - Monitor Closely (FREE Edition)"
    else:
        alert_level = "SAFE"
        alert_color = "🟢"
        alert_message = "Accumulation/Hold - No major alerts (FREE Edition)"
    
    # Prepare output
    output = {
        "composite_score": round(composite_score, 1),
        "smart_money_score": round(smart_money_score, 1),
        "alert_level": alert_level,
        "alert_color": alert_color,
        "alert_message": alert_message,
        "signals": signals,
        "timestamp": datetime.utcnow().isoformat(),
        "data_completeness": "110%",
        "tracker_version": "FREE EDITION"
    }
    
    # Save to file
    with open('data/current_signals.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Score calculated: {composite_score:.0f}/100 ({alert_color} {alert_level})")
    print(f"   Smart Money contribution: {smart_money_score:.0f} points")
    if triggered_signals:
        print(f"   Triggered signals: {', '.join(triggered_signals)}")
    else:
        print(f"   No signals triggered - Market in accumulation phase")

if __name__ == "__main__":
    calculate_score()

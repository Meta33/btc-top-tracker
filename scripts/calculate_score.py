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
    
    # Define signals with weights
    signals = [
        # TIER 1: Price & Market (25%)
        {
            "name": "BTC Price vs ATH",
            "weight": 0.20,
            "trigger": price_ratio >= 0.80,
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
            "name": "⛏️ Hash Rate Falling",
            "weight": 0.10,
            "trigger": data.get("hash_rate_trend", {}).get("declining", False),
            "current_value": f"{data.get('hash_rate_trend', {}).get('change_pct', 0):+.1f}%" if data.get('hash_rate_trend') else "N/A",
            "target": "< -10% (Miner capitulation)",
            "triggered": data.get("hash_rate_trend", {}).get("declining") if data.get('hash_rate_trend', {}).get("declining") is not None else None,
            "category": "Smart Money"
        },
        
        # TIER 3: Macro Context (25%)
        {
            "name": "SPX Rollover",
            "weight": 0.15,
            "trigger": data.get("spx_rollover", False),
            "current_value": f"${data.get('spx_price', 0):,.0f}" if data.get('spx_price') else "N/A",
            "target": "< 200-day MA (Risk-off)",
            "triggered": data.get("spx_rollover") if data.get("spx_rollover") is not None else None,
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
            "trigger": data.get("total2", 0) > 2_000_000_000_000,
            "current_value": f"${data.get('total2', 0) / 1e12:.2f}T",
            "target": "> $2T (Altcoin mania)",
            "triggered": data.get("total2", 0) > 2_000_000_000_000,
            "category": "Macro"
        }
    ]
    
    # Calculate scores
    composite_score = 0
    triggered_weight = 0
    available_weight = 0
    
    smart_money_score = 0
    smart_money_available = 0
    
    for signal in signals:
        if signal["triggered"] is not None:
            available_weight += signal["weight"]
            
            if signal["category"] == "Smart Money":
                smart_money_available += signal["weight"]
            
            if signal["triggered"]:
                triggered_weight += signal["weight"]
                
                if signal["category"] == "Smart Money":
                    smart_money_score += signal["weight"]
    
    if available_weight > 0:
        composite_score = (triggered_weight / available_weight) * 100
    else:
        composite_score = 0
    
    if smart_money_available > 0:
        smart_money_pct = (smart_money_score / smart_money_available) * 100
    else:
        smart_money_pct = None
    
    # Alert levels
    if composite_score >= 70:
        alert_level = "RED ALERT"
        alert_color = "🔴"
        alert_message = "FREE Smart Money signals showing DISTRIBUTION - High risk"
    elif composite_score >= 50:
        alert_level = "ORANGE"
        alert_color = "🟠"
        alert_message = "Distribution Phase - FREE signals warning"
    elif composite_score >= 30:
        alert_level = "YELLOW"
        alert_color = "🟡"
        alert_message = "Early Warning - Monitor FREE signals"
    else:
        alert_level = "SAFE"
        alert_color = "🟢"
        alert_message = "Accumulation/Hold - No major alerts (FREE Edition)"
    
    result = {
        "composite_score": round(composite_score, 1),
        "smart_money_score": round(smart_money_pct, 1) if smart_money_pct is not None else None,
        "alert_level": alert_level,
        "alert_color": alert_color,
        "alert_message": alert_message,
        "signals": signals,
        "timestamp": datetime.now().isoformat(),
        "data_completeness": f"{(available_weight / 1.0) * 100:.0f}%",
        "tracker_version": "FREE EDITION"
    }
    
    # Save
    with open('data/current_signals.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Composite Score: {composite_score:.1f}/100")
    if smart_money_pct is not None:
        print(f"   Smart Money Score: {smart_money_pct:.1f}/100 (FREE)")
    print(f"   Alert Level: {alert_color} {alert_level}")
    print(f"   Data Completeness: {result['data_completeness']}")
    print(f"   Tracker: 🆓 FREE EDITION ($0/month)")
    
    return result

if __name__ == "__main__":
    calculate_score()

#!/usr/bin/env python3
"""
Calculate composite score from fetched data
"""
import json
from datetime import datetime

def calculate_score():
    """Calculate weighted composite score"""
    
    # Load latest data
    with open('data/latest_data.json', 'r') as f:
        data = json.load(f)
    
    # Define signals with weights
    signals = [
        {
            "name": "BTC < $100K",
            "weight": 0.30,
            "triggered": data.get("btc_price", 999999) < 100000,
            "current_value": f"${data.get('btc_price', 0):,.0f}",
            "target": "< $100,000"
        },
        {
            "name": "LTH Distribution Elevated",
            "weight": 0.25,
            "triggered": data.get("lth_elevated", False),
           "current_value": f"{data.get('lth_distribution')} BTC/day" if data.get('lth_distribution') else "N/A",
            "target": "< -50,000 BTC/day"
        },
        {
            "name": "SPX Rollover",
            "weight": 0.15,
            "triggered": data.get("spx_price", 999999) < 6500,
            "current_value": f"{data.get('spx_price', 0):,.0f}",
            "target": "< 6,500"
        },
        {
            "name": "BTC Death Cross",
            "weight": 0.10,
            "triggered": data.get("btc_death_cross", False),
            "current_value": f"MA50: ${data.get('btc_ma50', 0):,.0f}, MA200: ${data.get('btc_ma200', 0):,.0f}",
            "target": "MA50 < MA200"
        },
        {
            "name": "M2 Growth Negative",
            "weight": 0.10,
            "triggered": data.get("m2_negative", False),
            "current_value": f"{data.get('m2_yoy_growth', 0):.1f}% YoY",
            "target": "< 0% YoY"
        },
        {
            "name": "BTC Dominance > 55%",
            "weight": 0.05,
            "triggered": data.get("btc_dominance", 0) > 55,
            "current_value": f"{data.get('btc_dominance', 0):.1f}%",
            "target": "> 55% on Mar 31"
        },
        {
            "name": "TOTAL2 < $2T",
            "weight": 0.05,
            "triggered": data.get("total2", 999999999999) < 2_000_000_000_000,
            "current_value": f"${data.get('total2', 0) / 1e12:.2f}T",
            "target": "< $2T on Mar 31"
        }
    ]
    
    # Calculate composite score
    composite_score = sum(s["weight"] * 100 for s in signals if s["triggered"])
    
    # Determine alert level
    if composite_score >= 70:
        alert_level = "🔴 RED ALERT"
        alert_color = "red"
    elif composite_score >= 50:
        alert_level = "🟠 ORANGE ALERT"
        alert_color = "orange"
    elif composite_score >= 30:
        alert_level = "🟡 YELLOW ALERT"
        alert_color = "yellow"
    else:
        alert_level = "🟢 SAFE"
        alert_color = "brightgreen"
    
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "composite_score": composite_score,
        "alert_level": alert_level,
        "alert_color": alert_color,
        "signals": signals,
        "triggered_count": sum(1 for s in signals if s["triggered"]),
        "total_count": len(signals)
    }
    
    # Save results
    with open('data/current_signals.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    # Append to history
    try:
        with open('data/historical_scores.csv', 'a') as f:
            f.write(f"{datetime.utcnow().isoformat()},{composite_score},{alert_level}\n")
    except:
        with open('data/historical_scores.csv', 'w') as f:
            f.write("timestamp,score,alert_level\n")
            f.write(f"{datetime.utcnow().isoformat()},{composite_score},{alert_level}\n")
    
    print(f"✅ Score calculated: {composite_score:.1f}% ({alert_level})")
    return result

if __name__ == "__main__":
    calculate_score()

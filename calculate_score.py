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
            "name": "BTC Price vs ATH",
            "weight": 0.30,
            "trigger": data.get("btc_price", 0) > 126280,  # Above Oct 6 ATH
            "current_value": f"${data.get('btc_price', 0):,.0f}",
            "target": "> $126K",
            "triggered": data.get("btc_price", 0) > 126280
        },
        {
            "name": "LTH Distribution Elevated",
            "weight": 0.25,
            "trigger": data.get("lth_elevated", False),
            "current_value": f"{data.get('lth_distribution', 'N/A')} BTC/day" if data.get('lth_distribution') else "N/A",
            "target": "> 3x baseline",
            "triggered": data.get("lth_elevated", False) if data.get("lth_elevated") is not None else None
        },
        {
            "name": "SPX Rollover",
            "weight": 0.15,
            "trigger": data.get("spx_rollover", False),
            "current_value": f"${data.get('spx_price', 0):,.0f}" if data.get('spx_price') else "N/A",
            "target": "< 200-day MA",
            "triggered": data.get("spx_rollover", False) if data.get("spx_rollover") is not None else None
        },
        {
            "name": "M2 Growth Slowing",
            "weight": 0.10,
            "trigger": data.get("m2_slowing", False),
            "current_value": f"{data.get('m2_growth', 0):.1f}% YoY" if data.get('m2_growth') else "N/A",
            "target": "< 5% YoY",
            "triggered": data.get("m2_slowing", False) if data.get("m2_slowing") is not None else None
        },
        {
            "name": "BTC Dominance Low",
            "weight": 0.10,
            "trigger": data.get("btc_dominance", 100) < 45,
            "current_value": f"{data.get('btc_dominance', 0):.1f}%",
            "target": "< 45%",
            "triggered": data.get("btc_dominance", 100) < 45
        },
        {
            "name": "USDT Dominance Low",
            "weight": 0.05,
            "trigger": data.get("usdt_dominance", 100) < 3,
            "current_value": f"{data.get('usdt_dominance', 0):.1f}%",
            "target": "< 3%",
            "triggered": data.get("usdt_dominance", 100) < 3
        },
        {
            "name": "TOTAL2 Peak",
            "weight": 0.05,
            "trigger": data.get("total2", 0) > 2_000_000_000_000,  # $2T
            "current_value": f"${data.get('total2', 0) / 1e12:.2f}T",
            "target": "> $2T",
            "triggered": data.get("total2", 0) > 2_000_000_000_000
        }
    ]
    
    # Calculate composite score (0-100)
    composite_score = 0
    triggered_weight = 0
    available_weight = 0
    
    for signal in signals:
        if signal["triggered"] is not None:  # Only count available signals
            available_weight += signal["weight"]
            if signal["triggered"]:
                triggered_weight += signal["weight"]
    
    # Normalize to 0-100 scale based on available data
    if available_weight > 0:
        composite_score = (triggered_weight / available_weight) * 100
    else:
        composite_score = 0
    
    # Determine alert level
    if composite_score >= 70:
        alert_level = "RED ALERT"
        alert_color = "🔴"
        alert_message = "High probability cycle top - Consider taking profits"
    elif composite_score >= 50:
        alert_level = "ORANGE"
        alert_color = "🟠"
        alert_message = "Elevated risk - Monitor closely"
    elif composite_score >= 30:
        alert_level = "YELLOW"
        alert_color = "🟡"
        alert_message = "Early warning - Watch for confirmation"
    else:
        alert_level = "SAFE"
        alert_color = "🟢"
        alert_message = "Hold position - No immediate top signals"
    
    # Prepare output
    result = {
        "composite_score": round(composite_score, 1),
        "alert_level": alert_level,
        "alert_color": alert_color,
        "alert_message": alert_message,
        "signals": signals,
        "timestamp": datetime.utcnow().isoformat(),
        "data_completeness": f"{(available_weight / 1.0) * 100:.0f}%"  # Percentage of available data
    }
    
    # Save results
    with open('data/current_signals.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Composite Score: {composite_score:.1f}/100")
    print(f"   Alert Level: {alert_color} {alert_level}")
    print(f"   Data Completeness: {result['data_completeness']}")
    
    return result

if __name__ == "__main__":
    calculate_score()

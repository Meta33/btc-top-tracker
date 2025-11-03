#!/usr/bin/env python3
"""
Update README with latest data
"""

import json
from datetime import datetime
import re

def update_readme():
    """Update README.md with latest signals"""
    
    # Load data
    with open('data/current_signals.json', 'r') as f:
        signals_data = json.load(f)
    
    # Read current README
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Format timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    # Update composite score badge
    score = signals_data['composite_score']
    if score >= 70:
        score_color = "red"
    elif score >= 50:
        score_color = "orange"
    elif score >= 30:
        score_color = "yellow"
    else:
        score_color = "brightgreen"
    
    score_badge = f"![Score](https://img.shields.io/badge/Score-{int(score)}%25-{score_color})"
    
    # Update alert level
    alert_color = signals_data['alert_color']
    alert_level = signals_data['alert_level']
    alert_message = signals_data['alert_message']
    
    # Build signal table
    table_rows = []
    for signal in signals_data['signals']:
        status_emoji = "🔴" if signal['triggered'] is True else ("🟢" if signal['triggered'] is False else "⏳")
        weight_pct = f"{signal['weight'] * 100:.0f}%"
        
        table_rows.append(
            f"| {signal['name']} | {weight_pct} | {signal['current_value']} | {signal['target']} | {status_emoji} |"
        )
    
    signal_table = "\n".join(table_rows)
    
    # Update README sections using regex
    
    # Update composite score section
    new_composite = f"Composite Score: {score_badge}\n\nAlert Level: {alert_color} **{alert_level}** - {alert_message}\n\nLast Updated: Auto-updates every 6 hours via GitHub Actions"
    readme = re.sub(
        r'Composite Score:.*?Last Updated: Auto-updates every 6 hours via GitHub Actions',
        new_composite,
        readme,
        flags=re.DOTALL
    )
    
    # Update signal table
    table_header = "| Signal | Weight | Current Value | Target | Status |"
    table_separator = "|--------|--------|---------------|--------|--------|"
    new_table = f"{table_header}\n{table_separator}\n{signal_table}"
    
    readme = re.sub(
        r'\| Signal \| Weight \| Current Value \| Target \| Status \|.*?(?=\n\n##|\n\n⚠️|$)',
        new_table,
        readme,
        flags=re.DOTALL
    )
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print(f"✅ README updated at {timestamp}")
    print(f"   Score: {score:.1f}/100 | Alert: {alert_level}")
    
    # Create GitHub Issue if RED ALERT
    if score >= 70:
        print("🚨 RED ALERT - Consider creating GitHub Issue for notification")

if __name__ == "__main__":
    update_readme()

!/usr/bin/env python3
"""
Update README.md with latest signal data - FREE SMART MONEY EDITION
"""

import json
import re
from datetime import datetime

def update_readme():
    """Update README.md with latest calculated signals"""
    
    # Load current signals
    with open('data/current_signals.json', 'r') as f:
        data = json.load(f)
    
    # Read current README
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Extract values
    composite_score = data['composite_score']
    alert_level = data['alert_level']
    alert_color = data['alert_color']
    alert_message = data['alert_message']
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())
    
    # Format timestamp (convert from ISO to readable)
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt.strftime('%Y-%m-%d %H:%M UTC')
    except:
        formatted_time = timestamp
    
    # Update composite score line
    score_pattern = r'Composite Score:.*'
    score_replacement = f'Composite Score: {composite_score:.0f} {alert_color}'
    readme = re.sub(score_pattern, score_replacement, readme)
    
    # Update alert level line
    alert_pattern = r'Alert Level:.*'
    alert_replacement = f'Alert Level: {alert_color} {alert_level}'
    readme = re.sub(alert_pattern, alert_replacement, readme)
    
    # Update timestamp line
    timestamp_pattern = r'Last Updated:.*'
    timestamp_replacement = f'Last Updated: {formatted_time} (Auto-updates every 6 hours)'
    readme = re.sub(timestamp_pattern, timestamp_replacement, readme)
    
    # Update alert message in the callout box
    message_pattern = r'(> \*\*Alert:\*\* ).*'
    message_replacement = f'\\1{alert_message}'
    readme = re.sub(message_pattern, message_replacement, readme)
    
    # Update signal table
    # Find the table section between "## Current Signals" and the next "##" or end
    table_start = readme.find('## Current Signals')
    if table_start != -1:
        # Find where table ends (next ## section or end of file)
        table_end = readme.find('\n##', table_start + 1)
        if table_end == -1:
            table_end = len(readme)
        
        # Build new table
        table_lines = [
            '## Current Signals',
            '',
            '| Status | Signal | Weight | Current Value |',
            '|--------|--------|--------|---------------|'
        ]
        
        # Add signal rows
        for signal in data['signals']:
            # Determine status emoji
            triggered = signal.get('triggered')
            if triggered is None:
                status = '⚪'  # Data unavailable
            elif triggered:
                status = '🔴'  # Triggered
            else:
                status = '🟢'  # Safe
            
            # Format weight
            weight_pct = f"{signal['weight']*100:.0f}%"
            
            # Format current value (handle None values)
            current_val = signal.get('current_value', 'N/A')
            if current_val is None:
                current_val = 'N/A'
            
            # Add row
            row = f"| {status} | {signal['name']} | {weight_pct} | {current_val} |"
            table_lines.append(row)
        
        # Add target column info
        table_lines.extend([
            '',
            '<details>',
            '<summary>📊 Signal Targets (Click to expand)</summary>',
            '',
            '| Signal | Target Condition |',
            '|--------|------------------|'
        ])
        
        for signal in data['signals']:
            target = signal.get('target', 'N/A')
            row = f"| {signal['name']} | {target} |"
            table_lines.append(row)
        
        table_lines.extend([
            '',
            '</details>',
            ''
        ])
        
        # Replace table section
        new_table = '\n'.join(table_lines)
        readme = readme[:table_start] + new_table + readme[table_end:]
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print(f"✅ README.md updated successfully")
    print(f"   Score: {composite_score:.0f}/100 ({alert_color} {alert_level})")
    print(f"   Message: {alert_message}")

if __name__ == "__main__":
    update_readme()

#!/usr/bin/env python3
"""
Update README.md with latest data
"""
import json

with open('data/current_signals.json', 'r', encoding='utf-8') as f:
    signals = json.load(f)

score = signals['composite_score']
emoji = signals['alert_color']  # Already contains 🟢

# Write to README
readme_content = f"Composite Score: {score} {emoji}\n"
readme_content += f"Alert Level: {emoji} {signals['alert_level']}\n"
    
    # Load current signals
    with open('data/current_signals.json', 'r') as f:
        data = json.load(f)
    
    # Read current README
    with open('README.md', 'r') as f:
        readme = f.read()
    
    # Update composite score badge
    score = data['composite_score']
    color = data['alert_color']
    badge_pattern = r'!\[Score\]\(https://img\.shields\.io/badge/Score-.*?-.*?\)'
    new_badge = f"![Score](https://img.shields.io/badge/Score-{score:.0f}%25-{color})"
    readme = re.sub(badge_pattern, new_badge, readme)
    
    # Update alert level
    alert_pattern = r'\*\*Alert Level:\*\* .*'
    new_alert = f"**Alert Level:** {data['alert_level']}"
    readme = re.sub(alert_pattern, new_alert, readme)
    
    # Update last updated timestamp
    timestamp_pattern = r'\*\*Last Updated:\*\* .*'
    new_timestamp = f"**Last Updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} (Auto-updates every 6 hours)"
    readme = re.sub(timestamp_pattern, new_timestamp, readme)
    
    # Update signal table (find table and replace rows)
    table_start = readme.find('| Signal | Weight | Current Value |')
    if table_start != -1:
        table_end = readme.find('\n---\n', table_start)
        
        # Build new table rows
        new_rows = []
        for signal in data['signals']:
            status = "✅" if signal['triggered'] else "❌"
            weight = f"{signal['weight']*100:.0f}%"
            row = f"| {signal['name']} | {weight} | {signal['current_value']} | {signal['target']} | {status} | Auto |"
            new_rows.append(row)
        
        # Find header line
        header_end = readme.find('\n', readme.find('|-----', table_start))
        table_header = readme[table_start:header_end+1]
        separator = readme[header_end+1:readme.find('\n', header_end+1)+1]
        
        new_table = table_header + separator + '\n'.join(new_rows) + '\n'
        
        # Replace old table
        old_table = readme[table_start:table_end]
        readme = readme.replace(old_table, new_table)
    
    # Update final timestamp at bottom
    final_pattern = r'\*\*Last Auto-Update:\*\* .*'
    final_timestamp = f"**Last Auto-Update:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    readme = re.sub(final_pattern, final_timestamp, readme)
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print(f"✅ README updated successfully")

if __name__ == "__main__":
    update_readme()

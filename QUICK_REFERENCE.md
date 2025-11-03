# 📋 Quick Reference Card

## Repository URL
`https://github.com/YOUR_USERNAME/btc-top-tracker`

## Check Status
Just visit your repository - README shows live data

## Alert Levels
- 🟢 0-30%: SAFE (Hold)
- 🟡 30-50%: YELLOW (Watch)
- 🟠 50-70%: ORANGE (Reduce 25-50%)
- 🔴 70%+: RED ALERT (Exit 50-75%)

## Update Schedule
Every 6 hours automatically

## Manual Trigger
Actions → "Update BTC Top Tracker" → "Run workflow"

## Notifications
Watch → Custom → Issues (enabled)

## Files to Edit
- `.github/workflows/update.yml` - Update frequency
- `scripts/calculate_score.py` - Signal weights/thresholds
- `README.md` - Dashboard text (auto-updates)

## Cost
$0/month (FREE forever with GitHub Actions)

## Support
Open an Issue in your repository


# 🚨 Bitcoin Cycle Top Tracker - Live Dashboard

**Automated tracking system for Bitcoin cycle top confirmation signals**

[![Update Data](https://github.com/YOUR_USERNAME/btc-top-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/YOUR_USERNAME/btc-top-tracker/actions/workflows/update.yml)

---

## 📊 Current Status

### **Composite Score: ![Score](https://img.shields.io/badge/Score-0%25-🟢)**

**Alert Level:** SAFE

**Last Updated:** 2025-11-04 02:33 UTC (Auto-updates every 6 hours)

---

## 🎯 Signal Dashboard

| Signal | Weight | Current Value | Target | Status | Last Check |
|--------|--------|---------------|--------|--------|------------|
| BTC Price vs ATH | 30% | $107,115 | > $126K (Oct 6 ATH) | ❌ | Auto |
| BTC Price vs ATH | 30% | $106,926 | > $126K (Oct 6 ATH) | ❌ | Auto |
| BTC Dominance Low | 5% | 58.6% | < 45% (Alt euphoria) | ❌ | Auto |
| 🔥 Volume Spike Alert | 25% | $0.34B/day | > 50% above baseline (Distribution) | ❌ | Auto |
| 📉 Market Cap Declining | 15% | +0.3% | < -5% (Smart money exiting) | ❌ | Auto |
| ⛏️ Hash Rate Falling | 10% | -1.5% | < -10% (Miner capitulation) | ❌ | Auto |
| SPX Rollover | 15% | $6,852 | < 200-day MA (Risk-off) | ❌ | Auto |
| USDT Dominance Low | 5% | 5.0% | < 3% (Liquidity exhaustion) | ❌ | Auto |
| TOTAL2 Peak | 5% | $1.51T | > $2T (Altcoin mania) | ❌ | Auto |

---

## 📈 Historical Score Chart

```
Score Progression (Last 30 Days):
100% ┤
 90% ┤
 80% ┤
 70% ┤ ← RED ALERT
 60% ┤
 50% ┤ ← ORANGE ALERT
 40% ┤
 30% ┤ ← YELLOW ALERT
 20% ┤
 10% ┤
  0% ┼────────────────────────────────────
     Nov 3    Nov 10    Nov 17    Nov 24
```

---

## 🚨 Alert Thresholds

| Score Range | Alert Level | Action Required |
|-------------|-------------|-----------------|
| 0-30% | 🟢 **SAFE** | HOLD position, continue DCA |
| 30-50% | 🟡 **YELLOW ALERT** | Watch closely, prepare exit plan |
| 50-70% | 🟠 **ORANGE ALERT** | Reduce position 25-50% |
| 70%+ | 🔴 **RED ALERT** | EXIT 50-75% immediately |

---

## 🔔 Getting Notifications

### Option 1: Watch This Repository
1. Click "Watch" → "Custom" → "Issues"
2. GitHub Actions will create an Issue when score hits 70%+

### Option 2: RSS Feed
Subscribe to: `https://github.com/YOUR_USERNAME/btc-top-tracker/commits/main.atom`

### Option 3: Telegram Bot (Advanced)
See [TELEGRAM_SETUP.md](./docs/TELEGRAM_SETUP.md)

### Option 4: Discord Webhook (Advanced)
See [DISCORD_SETUP.md](./docs/DISCORD_SETUP.md)

---

## 📁 Repository Structure

```
btc-top-tracker/
├── .github/
│   └── workflows/
│       └── update.yml          # GitHub Actions workflow (runs every 6 hours)
├── scripts/
│   ├── fetch_data.py           # Fetches live market data
│   ├── calculate_score.py      # Calculates composite score
│   └── update_readme.py        # Updates this README
├── data/
│   ├── current_signals.json    # Latest signal values
│   ├── historical_scores.csv   # Score history for charts
│   └── config.yaml            # API keys and thresholds
├── docs/
│   ├── TELEGRAM_SETUP.md       # Telegram bot instructions
│   └── DISCORD_SETUP.md        # Discord webhook instructions
├── README.md                   # This file (auto-updated)
└── requirements.txt            # Python dependencies

```

---

## 🚀 Setup Instructions

### 1. Fork This Repository
Click "Fork" at the top right of this page

### 2. Enable GitHub Actions
1. Go to "Settings" → "Actions" → "General"
2. Set "Workflow permissions" to "Read and write permissions"
3. Click "Save"

### 3. Add API Keys (Optional - For Full Automation)
Go to "Settings" → "Secrets and variables" → "Actions" → "New repository secret"

**Free APIs (No signup needed):**
- None required for basic functionality!

**Paid APIs (For advanced features):**
- `GLASSNODE_API_KEY` - For LTH distribution ($29/mo)
- `COINMARKETCAP_API_KEY` - For market data (Free tier available)

**Note:** Without API keys, the tracker uses free public endpoints (CoinGecko, TradingView public charts)

### 4. Manual Trigger (Optional)
- Go to "Actions" → "Update BTC Top Tracker"
- Click "Run workflow" → "Run workflow"
- First run will initialize all data

### 5. Star This Repository ⭐
Stay updated with changes and improvements

---

## 🔧 How It Works

### GitHub Actions Workflow (Automated)

**Schedule:** Every 6 hours (adjustable in `.github/workflows/update.yml`)

**Process:**
1. ✅ Fetch live Bitcoin price from CoinGecko API
2. ✅ Fetch S&P 500 data from Yahoo Finance
3. ✅ Fetch BTC dominance from TradingView
4. ✅ Fetch TOTAL2 from CoinGecko
5. ✅ Calculate moving averages for Death Cross
6. ✅ Check M2 data from FRED (monthly)
7. ✅ Fetch LTH data from Glassnode OR CryptoQuant
8. ✅ Calculate composite score (weighted average)
9. ✅ Update README.md with latest values
10. ✅ Commit changes to repository
11. ✅ Create GitHub Issue if score > 70%

**Total runtime:** ~2-3 minutes per update

---

## 📊 Data Sources

All data sources are verified and credible:

| Metric | Source | Update Frequency |
|--------|--------|------------------|
| BTC Price | [CoinGecko API](https://www.coingecko.com/) | Real-time |
| SPX Price | [Yahoo Finance](https://finance.yahoo.com/) | Real-time |
| BTC Dominance | [CoinGecko API](https://www.coingecko.com/) | Real-time |
| TOTAL2 | [CoinGecko API](https://www.coingecko.com/) | Real-time |
| Moving Averages | Calculated from historical data | Daily |
| M2 Money Supply | [FRED API](https://fred.stlouisfed.org/) | Monthly |
| LTH Distribution | [Glassnode](https://glassnode.com/) OR [CryptoQuant](https://cryptoquant.com/) | Daily |

---

## 📱 Mobile Access

**View on mobile:**
1. Save this repository to your GitHub mobile app favorites
2. Enable notifications for Issues
3. Check anytime at: `https://github.com/YOUR_USERNAME/btc-top-tracker`

**Or create a mobile shortcut:**
- iOS: Add to Home Screen via Safari
- Android: Add to Home Screen via Chrome

---

## 🔒 Privacy & Security

- ✅ **No personal data collected**
- ✅ **Open source code** - audit everything
- ✅ **Runs on GitHub infrastructure** - free forever
- ✅ **No tracking or analytics**
- ✅ **API keys stored securely** in GitHub Secrets

---

## 📈 Cost Analysis

**GitHub-based tracker:**
- GitHub Actions: **FREE** (2,000 minutes/month on free plan)
- This tracker uses ~720 minutes/month (6 updates/day × 30 days × 3 min)
- Storage: Negligible (<1MB)
- **Total cost: $0/month** ✅

**With optional paid APIs:**
- Glassnode Starter: $29/mo (better LTH data)
- CoinMarketCap Pro: $0 (free tier sufficient)
- **Total: $0-29/month**

**Compare to manual tracking:**
- Time saved: ~10 hours/month
- Peace of mind: Priceless

---

## 🤝 Contributing

Found a bug or have a feature request?
1. Open an Issue
2. Submit a Pull Request
3. Join discussions

---

## 📜 License

MIT License - Free to use, modify, and distribute

---

## ⚠️ Disclaimer

This tracker is for educational and informational purposes only. Not financial advice.
Always do your own research and consult with a financial advisor before making investment decisions.

---

## 🙏 Credits

- **Analysis methodology:** Based on comprehensive Bitcoin cycle top research
- **Data sources:** CoinGecko, Yahoo Finance, FRED, Glassnode, CryptoQuant
- **Built with:** Python, GitHub Actions, Markdown

---

## 📞 Support

- **Issues:** [Open a GitHub Issue](https://github.com/YOUR_USERNAME/btc-top-tracker/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/btc-top-tracker/discussions)

---

**Last Auto-Update:** 2025-11-04 02:33:26 UTC

**Next Update:** In ~6 hours

---

⭐ **Star this repository to stay updated!** ⭐


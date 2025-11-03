# 🚀 GitHub Tracker Setup Guide

## Complete Step-by-Step Instructions

### Total Setup Time: 10 minutes

---

## ✅ Step 1: Create Your GitHub Repository (2 min)

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Name it: `btc-top-tracker` (or any name you like)
4. Set to **Public** (required for free GitHub Actions)
5. ✅ Check "Add a README file"
6. Click **"Create repository"**

---

## ✅ Step 2: Upload Files (3 min)

### Option A: Using GitHub Web Interface (Easiest)

1. Download the ZIP file from your AI Drive
2. Extract all files locally
3. In your GitHub repository, click **"Add file"** → **"Upload files"**
4. Drag and drop ALL files and folders from the extracted ZIP
5. Scroll down, add commit message: "Initial setup"
6. Click **"Commit changes"**

### Option B: Using Git Command Line

```bash
# Download ZIP from AI Drive, extract it, then:
cd btc-top-tracker
git init
git add .
git commit -m "Initial setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/btc-top-tracker.git
git push -u origin main
```

---

## ✅ Step 3: Enable GitHub Actions (2 min)

1. Go to your repository → **"Settings"** tab
2. Left sidebar → **"Actions"** → **"General"**
3. Under "Workflow permissions":
   - Select ✅ **"Read and write permissions"**
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"
4. Click **"Save"**

---

## ✅ Step 4: Add API Keys (Optional - 2 min)

**Note:** The tracker works WITHOUT API keys using free public endpoints!

### If you want enhanced LTH data (optional):

1. Go to **"Settings"** → **"Secrets and variables"** → **"Actions"**
2. Click **"New repository secret"**
3. Add:
   - Name: `GLASSNODE_API_KEY`
   - Value: Your Glassnode API key (from [studio.glassnode.com](https://studio.glassnode.com))
4. Click **"Add secret"**

---

## ✅ Step 5: Run First Update (1 min)

1. Go to **"Actions"** tab in your repository
2. Left sidebar → Click **"Update BTC Top Tracker"**
3. Right side → **"Run workflow"** button → **"Run workflow"**
4. Wait 2-3 minutes
5. ✅ Check that README.md updated with live data

---

## ✅ Step 6: Enable Notifications (2 min)

### Get RED ALERT notifications:

1. Click **"Watch"** button (top right of repository)
2. Select **"Custom"**
3. ✅ Check **"Issues"**
4. Click **"Apply"**

Now you'll receive email when score hits 70%+!

### Optional: Mobile notifications

1. Install **GitHub Mobile App**:
   - iOS: [App Store](https://apps.apple.com/app/github/id1477376905)
   - Android: [Play Store](https://play.google.com/store/apps/details?id=com.github.android)
2. Enable push notifications in app settings
3. You'll get instant alerts on your phone!

---

## 🎉 You're Done!

Your tracker will now:
- ✅ Auto-update every 6 hours
- ✅ Display live data on README
- ✅ Create GitHub Issue when score hits 70%+
- ✅ Send you email/mobile alerts
- ✅ Keep historical data in CSV
- ✅ Run completely FREE on GitHub

---

## 📱 How to Check Your Tracker

**Desktop:**
- Just visit: `https://github.com/YOUR_USERNAME/btc-top-tracker`
- Bookmark it for quick access

**Mobile:**
- Add to home screen in browser
- Or use GitHub mobile app

---

## ⚙️ Customization Options

### Change Update Frequency

Edit `.github/workflows/update.yml`, line 5:

```yaml
- cron: '0 */6 * * *'  # Every 6 hours (current)
- cron: '0 */1 * * *'  # Every hour
- cron: '0 */12 * * *' # Every 12 hours
- cron: '0 8,20 * * *' # Twice daily (8am & 8pm UTC)
```

### Change Alert Threshold

Edit `scripts/calculate_score.py`, find:

```python
if composite_score >= 70:  # Change 70 to your preferred threshold
```

### Add More Signals

Edit `scripts/calculate_score.py`, add to `signals` list:

```python
{
    "name": "Your Custom Signal",
    "weight": 0.05,  # 5% weight
    "triggered": your_condition_here,
    "current_value": f"{your_value}",
    "target": "Your target"
}
```

---

## 🔧 Troubleshooting

### GitHub Actions not running?

1. Check Settings → Actions → "Allow all actions"
2. Make sure "Read and write permissions" enabled
3. Try manual trigger: Actions → Run workflow

### README not updating?

1. Check Actions tab for error messages
2. Verify files are in correct folders
3. Make sure Python scripts have correct indentation

### No data showing?

1. Wait for first run to complete (2-3 min)
2. Check `data/current_signals.json` file exists
3. Check API rate limits (CoinGecko: 50 calls/min)

---

## 💰 Cost Breakdown

**FREE Forever:**
- GitHub Actions: 2,000 min/month free
- This tracker: ~720 min/month used
- Storage: <1MB (negligible)
- **Total: $0/month** ✅

**Optional Paid:**
- Glassnode API: $29/mo (better LTH data)
- But tracker works fine WITHOUT it!

---

## 🆘 Need Help?

1. **Check Actions tab** for error logs
2. **Open an Issue** in your repository
3. **Ask in discussions** (if enabled)

---

## 🎯 What Happens Next?

Every 6 hours, GitHub Actions will:
1. Fetch latest Bitcoin price, SPX, dominance, etc.
2. Calculate composite score
3. Update README with live data
4. Create Issue if score > 70%
5. Send you notification

**You don't have to do ANYTHING manually!**

Just check your repository occasionally, or wait for the RED ALERT notification.

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Repository created on GitHub
- [ ] All files uploaded correctly
- [ ] GitHub Actions enabled (Settings → Actions)
- [ ] First workflow run completed successfully
- [ ] README shows live data (not "Loading...")
- [ ] Watch enabled for Issues notifications
- [ ] Bookmarked repository URL

---

**Congratulations! You now have a professional, automated Bitcoin cycle top tracker running 24/7 for FREE!** 🎉

No more manual spreadsheets. No more missed signals. Just automated peace of mind.


# Crontab Configuration - Fixed & Optimized

## ❌ YOUR CURRENT CRONTAB (Missing -ee flag)

```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split >/dev/null 2>&1
```

**Issues:**
1. ❌ Missing `-ee` flag (no extra whois fallback)
2. ❌ Missing `-g` flag (no Google Chat notifications)
3. ⚠️ Using `-t` for Telegram but you want Google Chat now
4. ⚠️ Runs every 5 days at midnight (is this what you want?)

---

## ✅ FIXED VERSION 1: With Google Chat + Extra Whois

```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee >/dev/null 2>&1
```

**What changed:**
- ✅ Added `-ee` (extra whois checks - MOST IMPORTANT!)
- ✅ Added `-g` (Google Chat notifications)
- ✅ Removed `-t -trim -split` (Telegram-specific flags)

---

## ✅ FIXED VERSION 2: With Both Telegram AND Google Chat

If you want to keep Telegram notifications AND add Google Chat:

```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split -g -ee >/dev/null 2>&1
```

**What changed:**
- ✅ Added `-g` (Google Chat)
- ✅ Added `-ee` (extra whois checks)
- ✅ Kept `-t -trim -split` (Telegram still works)

---

## 🎯 RECOMMENDED VERSION (Most Reliable)

### Daily Check at 2 AM with Google Chat

```bash
0 2 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30 2>&1 | tee -a /var/log/domain-checker.log
```

**What this does:**
- ✅ Runs daily at 2 AM (not every 5 days)
- ✅ `-nb` = No banner (clean output)
- ✅ `-f aikyam.txt` = Your domain file
- ✅ `-i 10` = 10 second intervals (good for avoiding rate limits)
- ✅ `-g` = Google Chat notifications
- ✅ **`-ee`** = **Extra whois checks (CRITICAL!)** ⭐
- ✅ `-x 30` = Alert 30 days before expiry
- ✅ Saves logs to `/var/log/domain-checker.log`

---

## 📊 CRON SCHEDULE EXPLANATION

### Your Current: `0 0 */5 * *`
- Runs at: **00:00 (midnight)**
- Every: **5 days**
- Example: Jan 1, Jan 6, Jan 11, Jan 16, Jan 21, Jan 26, Jan 31

### Recommended: `0 2 * * *`
- Runs at: **02:00 (2 AM)**
- Every: **day**
- Example: Daily at 2 AM

### Alternative Options:

#### Every 3 days at 2 AM:
```bash
0 2 */3 * * /home/ubuntu/dns-domain-expiration-checker/./ddec ...
```

#### Twice daily (2 AM and 2 PM):
```bash
0 2,14 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec ...
```

#### Weekly (Sunday at 2 AM):
```bash
0 2 * * 0 /home/ubuntu/dns-domain-expiration-checker/./ddec ...
```

---

## 🔧 STEP-BY-STEP FIX ON YOUR VPS

### Step 1: Edit crontab
```bash
ssh ubuntu@your-vps
crontab -e
```

### Step 2: Replace old line with new line

#### OLD (remove this):
```
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split >/dev/null 2>&1
```

#### NEW (add this):
```
0 2 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30 2>&1 | tee -a /var/log/domain-checker.log
```

### Step 3: Save and exit
- If using nano: `Ctrl+X`, then `Y`, then `Enter`
- If using vim: `Esc`, then `:wq`, then `Enter`

### Step 4: Verify crontab
```bash
crontab -l
```

Should show your new line.

---

## 🔍 VERIFY WHOIS IS INSTALLED ON VPS

Before the cron runs, make sure whois is installed:

```bash
# SSH to your VPS
ssh ubuntu@your-vps

# Check if whois exists
which whois

# If it shows a path like /usr/bin/whois, you're good!
# If it says "not found", install it:
sudo apt update
sudo apt install whois -y
```

---

## 📝 COMPLETE COMPARISON

### Your Original Command Breakdown:
```bash
0 0 */5 * *                           # Every 5 days at midnight
/home/ubuntu/.../ddec                 # Script path ✅
-nb                                   # No banner ✅
-f /home/ubuntu/.../aikyam.txt        # Domain file ✅
-i 10                                 # 10 sec intervals ✅
-t                                    # Telegram notifications ✅
-trim                                 # Trim long Telegram messages ✅
-split                                # Split long Telegram messages ✅
                                      # ❌ MISSING: -ee (extra whois)
                                      # ❌ MISSING: -g (Google Chat)
>/dev/null 2>&1                       # Discard all output ⚠️
```

### Recommended Command Breakdown:
```bash
0 2 * * *                             # Daily at 2 AM ✅
/home/ubuntu/.../ddec                 # Script path ✅
-nb                                   # No banner ✅
-f /home/ubuntu/.../aikyam.txt        # Domain file ✅
-i 10                                 # 10 sec intervals ✅
-g                                    # Google Chat ✅ NEW!
-ee                                   # Extra whois checks ✅ NEW!
-x 30                                 # Alert 30 days before ✅ NEW!
2>&1 | tee -a /var/log/...            # Save logs ✅
```

---

## 🎯 QUICK ANSWER TO YOUR QUESTION

### "What else do I have to add for extra whois checks?"

**Just add `-ee` to your existing command:**

### Minimal Change (Keep everything else):
```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split -ee >/dev/null 2>&1
```

**That's it! Just add `-ee` at the end!**

---

## 💡 RECOMMENDED IMPROVEMENTS

### If you're updating anyway, consider this optimized version:

```bash
# Daily at 2 AM with Google Chat, Extra Whois, and Logs
0 2 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30 -twtc 2>&1 | tee -a /var/log/domain-checker.log
```

**Benefits:**
- ✅ Daily checks (more reliable than every 5 days)
- ✅ Google Chat notifications (your webhook works!)
- ✅ Extra whois checks (`-ee` - most important!)
- ✅ 30-day alert threshold (`-x 30`)
- ✅ Track WHOIS changes (`-twtc` - bonus!)
- ✅ Keeps logs for debugging

---

## 🔍 TEST BEFORE CRON

Before setting up cron, test the command manually:

```bash
# SSH to VPS
ssh ubuntu@your-vps

# Run the command manually
/home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30

# Watch for:
# 1. "whois found in: /usr/bin/whois" (confirms -ee will work)
# 2. Google Chat message appears in your space
# 3. No errors in output
```

---

## 📋 ENVIRONMENT VARIABLE FOR WEBHOOK (Optional Security)

Instead of hardcoding webhook in script, use environment variable in cron:

```bash
# Edit crontab
crontab -e

# Add this line at the top (before cron jobs):
GOOGLE_CHAT_WEBHOOK=https://chat.googleapis.com/v1/spaces/AAQAqk2vDYk/messages?key=...

# Then your cron job (webhook auto-picked from env var):
0 2 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30 2>&1 | tee -a /var/log/domain-checker.log
```

---

## 🚨 COMMON ISSUES & FIXES

### Issue 1: "whois: command not found"
**Fix:**
```bash
sudo apt install whois -y
```

### Issue 2: Cron doesn't run / no notifications
**Fix:**
```bash
# Check cron is running
sudo systemctl status cron

# Check cron logs
grep CRON /var/log/syslog | tail -20

# Test manually first
/home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee
```

### Issue 3: Permission denied
**Fix:**
```bash
# Make script executable
chmod +x /home/ubuntu/dns-domain-expiration-checker/ddec

# Check file ownership
ls -la /home/ubuntu/dns-domain-expiration-checker/ddec
```

### Issue 4: No Google Chat messages
**Fix:**
```bash
# Verify webhook is set in script
grep GOOGLE_CHAT_WEBHOOK /home/ubuntu/dns-domain-expiration-checker/ddec

# Test webhook manually (from earlier section)
# Or use environment variable method above
```

---

## ✅ FINAL RECOMMENDATION

### Choose ONE of these:

#### Option 1: Minimal Change (Just add -ee)
```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split -ee >/dev/null 2>&1
```

#### Option 2: Add Google Chat + Keep Telegram
```bash
0 0 */5 * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -t -trim -split -g -ee >/dev/null 2>&1
```

#### Option 3: Optimal (Daily, Google Chat, Logs) ⭐ RECOMMENDED
```bash
0 2 * * * /home/ubuntu/dns-domain-expiration-checker/./ddec -nb -f /home/ubuntu/dns-domain-expiration-checker/aikyam.txt -i 10 -g -ee -x 30 2>&1 | tee -a /var/log/domain-checker.log
```

---

## 🎯 SUMMARY

### To enable extra whois checks:

**Just add `-ee` to your existing crontab command!**

### Before:
```
... -i 10 -t -trim -split >/dev/null 2>&1
```

### After:
```
... -i 10 -t -trim -split -ee >/dev/null 2>&1
```

**That's literally all you need!** The rest is optional improvements. ✅

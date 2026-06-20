# DNS Domain Expiration Checker - Quick Reference Card

## 🚀 THE ONE COMMAND YOU NEED TO REMEMBER

```bash
python3 ddec.py -f aikyam.txt -g -ee -i 5
```

**This checks all domains with maximum reliability and sends to Google Chat**

---

## 📋 ESSENTIAL FLAGS

| Flag | What It Does | Example |
|------|-------------|---------|
| `-f FILE` | Domain list file | `-f aikyam.txt` |
| `-d DOMAIN` | Single domain | `-d aikyam.school` |
| `-g` | Google Chat notification | `-g` |
| `-w URL` | Google Chat webhook | `-w "https://..."` |
| **`-ee`** | **Extra external whois (RECOMMENDED!)** ⭐ | **`-ee`** |
| `-i SECONDS` | Interval between checks | `-i 5` |
| `-x DAYS` | Alert N days before expiry | `-x 30` |
| `-c` | Print to console | `-c` |
| `-l` | Long format (detailed) | `-l` |
| `-nb` | No banner (for cron) | `-nb` |
| `-e EMAIL` | Send email | `-e you@email.com` |
| `-t` | Telegram notification | `-t` |

---

## 💎 PRODUCTION COMMAND (Copy-Paste Ready)

```bash
# For VPS/Server (with all features)
python3 ddec.py \
  -f /path/to/aikyam.txt \
  -g \
  -ee \
  -i 5 \
  -x 30 \
  -nb
```

**What this does:**
- ✅ Checks all domains in `aikyam.txt`
- ✅ Uses internal + external WHOIS (most reliable)
- ✅ Sends notifications to Google Chat
- ✅ Waits 5 seconds between domains (avoids rate limits)
- ✅ Alerts 30 days before expiry
- ✅ No banner (clean output for logs)

---

## ⏰ CRON JOB (Run Daily)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/script && /usr/bin/python3 ddec.py -f aikyam.txt -g -ee -i 5 -nb >> /var/log/domain-check.log 2>&1
```

---

## 🧪 TEST COMMANDS

### Test Single Domain
```bash
python3 ddec.py -d aikyam.school -c -g -ee
```

### Test with Detailed Output
```bash
python3 ddec.py -d catsofkochi.com -c -l -g -ee
```

### Test Domain File (Console + Google Chat)
```bash
python3 ddec.py -f aikyam.txt -c -g -ee -i 3
```

### Test Without Sending Notifications (Console Only)
```bash
python3 ddec.py -f aikyam.txt -c -ee -i 3
```

---

## 📝 DOMAIN FILE FORMAT (aikyam.txt)

```
! My Domains
catsofkochi.com 30 cost:12.50
aikyam.school 60 cost:15.00
pattic.school 45 cost:15.00

! Client Domains
example.com 30
test.org 90 sleep:10
```

**Format:**
```
domain.com [days] [sleep:seconds] [cost:amount]
```

**Lines starting with:**
- `!` = Group header
- `#` = Comment (ignored)
- Empty lines = Ignored

---

## 🎯 WHOIS MODES EXPLAINED

### Default (Internal Only) - Not Recommended
```bash
python3 ddec.py -f aikyam.txt -g
```
- Fast but may fail on .school and newer TLDs
- 85% success rate

### External Only (-oe)
```bash
python3 ddec.py -f aikyam.txt -g -oe
```
- Slower, may show false alerts for regional registrars
- 95% success rate

### Internal + External Fallback (-ee) ⭐ RECOMMENDED
```bash
python3 ddec.py -f aikyam.txt -g -ee
```
- **Best reliability: 98% success rate**
- Fast + Fallback = Best of both worlds
- **ALWAYS USE THIS MODE!**

---

## 🔧 COMMON USE CASES

### Check .school Domains
```bash
python3 ddec.py -d aikyam.school -c -g -ee
```

### Multiple Notifications (Email + Google Chat)
```bash
python3 ddec.py -f aikyam.txt -e admin@aikyam.com -g -ee -i 5
```

### All Notifications (Email + Telegram + Google Chat)
```bash
python3 ddec.py -f aikyam.txt -e admin@aikyam.com -t -g -ee -i 5
```

### Track WHOIS Changes (Advanced)
```bash
python3 ddec.py -f aikyam.txt -g -ee -twtc -i 5
```
Detects if domain WHOIS info changes (registrar, contacts, etc.)

---

## 📧 EMAIL SETUP

### Gmail (App Password required — plain password blocked since May 2022)

1. Enable 2-Step Verification at myaccount.google.com
2. Go to Security → App Passwords → generate a 16-character password
3. Add to your `.env` file:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_SENDER=you@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop   # your 16-char app password (spaces ok)
EMAIL_TO=recipient@example.com
ENABLE_EMAIL_STARTTLS=true
ENABLE_EMAIL_AUTH=true
```

### Mailgun (SMTP credentials from your Mailgun Sending Domains page)

```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_SENDER=postmaster@mg.yourdomain.com
SMTP_PASSWORD=<Mailgun SMTP password>
EMAIL_TO=recipient@example.com
ENABLE_EMAIL_STARTTLS=true
ENABLE_EMAIL_AUTH=true
```

### Test email manually
```bash
# With .env configured:
python3 ddec_rdap.py -d aikyam.school -c

# Or fully via CLI flags (no .env needed):
python3 ddec_rdap.py -d aikyam.school \
  -e recipient@example.com \
  -starttls -auth -c
```

### Rules
- Use `-starttls` for port **587** (Gmail, Mailgun)
- Use `-ssl` for port **465** (some providers)
- Never use both `-ssl` and `-starttls` together
- Always add `-auth` when using Gmail or Mailgun

---

## 🔒 SECURITY: WEBHOOK URL

### Method 1: Environment Variable (Recommended)
```bash
# In ~/.bashrc or ~/.zshrc
export GOOGLE_CHAT_WEBHOOK="https://chat.googleapis.com/v1/spaces/..."

# Then just use
python3 ddec.py -f aikyam.txt -g -ee
```

### Method 2: Command Line
```bash
python3 ddec.py -f aikyam.txt -g -w "https://chat.googleapis.com/..." -ee
```

### Method 3: In Script (Less Secure)
Edit `ddec.py` line 195:
```python
GOOGLE_CHAT_WEBHOOK: str = "https://chat.googleapis.com/v1/spaces/..."
```

---

## 📊 INTERVAL RECOMMENDATIONS

| Domain Count | Recommended Interval |
|--------------|---------------------|
| < 10 domains | `-i 3` |
| 10-50 domains | `-i 5` |
| 50-100 domains | `-i 10` |
| 100+ domains | `-i 15` |

**Why?** Prevents WHOIS rate limiting and "too many requests" errors

---

## ⚠️ TROUBLESHOOTING

### Error: "Domain shows error"
**Solution:** Use `-ee` flag for fallback

### Error: "Connection limit exceeded"
**Solution:** Increase interval: `-i 10` or `-i 15`

### Error: "Google Chat webhook error"
**Solution:** Check webhook URL is correct

### Error: "whois command not found"
**Solution:** Install whois:
```bash
# Linux
sudo apt install whois

# macOS
brew install whois
```

### Warning: "timezone error"
**Workaround:** Script will still work, just ignore the warning

---

## 📁 FILE LOCATIONS

```
/path/to/
├── ddec.py                    # Main script
├── aikyam.txt                 # Your domain list
├── ddec-cache/                # WHOIS change tracking cache
└── /var/log/domain-check.log  # Log file (if using cron)
```

---

## 🎓 ADVANCED FEATURES

### Track WHOIS Text Changes
```bash
python3 ddec.py -f aikyam.txt -g -ee -twtc
```
Monitors changes in WHOIS data (registrar changes, contact updates, etc.)

### Custom Alert Threshold Per Domain
In `aikyam.txt`:
```
urgent.com 15        # Alert 15 days before
normal.com 30        # Alert 30 days before
relaxed.com 90       # Alert 90 days before
```

### Custom Sleep Per Domain
```
busy-registrar.com 30 sleep:15    # Wait 15 seconds for this one
normal.com 30 sleep:5             # Default 5 seconds
```

### Skip WHOIS Change Tracking for Specific Domain
```
stable.com 30 skip_checking_whois_text_changes
```

---

## ✅ BEST PRACTICES

1. **Always use `-ee` flag** for maximum reliability
2. **Use `-i 5` or higher** to avoid rate limits
3. **Set `-x 30`** (alert 30 days before) as minimum
4. **Use environment variable** for webhook URL (more secure)
5. **Run via cron daily** instead of real-time monitoring
6. **Keep logs** with `>> /var/log/domain-check.log 2>&1`
7. **Test first** with `-c` flag to see console output

---

## 🚨 THE GOLDEN RULE

**ALWAYS include the `-ee` flag for production use!**

```bash
✅ GOOD:  python3 ddec.py -f aikyam.txt -g -ee -i 5
❌ BAD:   python3 ddec.py -f aikyam.txt -g -i 5
```

The `-ee` flag ensures maximum reliability by using:
1. Internal engine first (fast)
2. External whois fallback (reliable)
3. Best success rate (98%)

---

## 📞 QUICK HELP

```bash
# Show all options
python3 ddec.py -h

# Show version
python3 ddec.py -v
```

---

## 📚 DOCUMENTATION FILES

- `GOOGLE_CHAT_CHANGES.md` - Google Chat implementation details
- `WHOIS_MODES_EXPLAINED.md` - Deep dive into -ee flag
- `DOMAIN_SUBMISSION_SOLUTIONS.md` - How users can submit domains
- `CHANGES_SUMMARY.txt` - Quick code changes reference
- `README.md` - Original documentation

---

**Happy domain monitoring! 🎉**

Remember: `-ee` is your friend for reliable checks!

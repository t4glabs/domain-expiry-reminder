# -ee Flag Setup Guide

## ✅ GOOD NEWS: ZERO CONFIGURATION NEEDED!

The `-ee` flag (extra external whois) is **100% ready to use** on your system right now!

---

## 🔍 System Check Results

### ✅ Whois is Installed
```
Location: /usr/bin/whois
Status: WORKING ✅
```

Your system already has `whois` installed and functioning properly.

---

## 🎯 How -ee Works (Automatically)

### When you run:
```bash
python3 ddec.py -f aikyam.txt -g -ee -i 5
```

### What happens behind the scenes:

```
For each domain in aikyam.txt:

1. Script tries INTERNAL python-whois library
   ├─ If SUCCESS → Use that result (fast!)
   └─ If ERROR → Continue to step 2

2. Script automatically calls: /usr/bin/whois domain.com
   ├─ Parses the output
   └─ Returns expiry date

3. Send notification to Google Chat
```

---

## 🔧 NO Setup Required!

### You DON'T need to:
- ❌ Configure anything
- ❌ Install additional software
- ❌ Set environment variables
- ❌ Modify the script
- ❌ Create config files

### You ONLY need to:
- ✅ Add the `-ee` flag to your command
- ✅ That's it!

---

## 📝 How the Script Finds Whois

The script automatically detects whois in this order:

### 1. Checks common locations:
```
/usr/bin/whois           ✅ (Found on your system!)
/usr/local/bin/whois
/opt/homebrew/bin/whois
```

### 2. Searches system PATH
If not found in common locations, searches all directories in your PATH environment variable.

### 3. Auto-configures
Script sets `WHOIS_COMMAND = "/usr/bin/whois"` automatically.

---

## ✅ Verification (Your System)

### When you ran the script earlier, you saw:
```
The whois found in: /usr/bin/whois
```

This means:
- ✅ Whois is installed
- ✅ Script detected it automatically
- ✅ Ready to use with `-ee` flag
- ✅ No configuration needed

---

## 🚀 Ready-to-Use Commands

### Test it right now:
```bash
# Single domain test
python3 ddec.py -d google.com -c -ee

# Your domain file
python3 ddec.py -f aikyam.txt -c -g -ee -i 5

# Production command
python3 ddec.py -f aikyam.txt -g -ee -i 5 -nb
```

---

## 🔍 How to Verify -ee is Working

### Method 1: Look for the banner message
When you run the script WITHOUT `-nb` flag, you'll see:

```
The whois found in: /usr/bin/whois
```

This confirms external whois is available.

### Method 2: Check console output
Run with `-c` flag and watch the domains being processed:

```bash
python3 ddec.py -f aikyam.txt -c -ee -i 3
```

You'll see domains being checked. If internal fails, external whois kicks in automatically.

### Method 3: Test a domain that requires external whois
```bash
python3 ddec.py -d aikyam.school -c -ee
```

`.school` domains often need external whois, so this tests the fallback mechanism.

---

## 💡 What Happens on VPS?

### On your VPS server, the script will:

1. **Auto-detect whois location** on first run
2. **Check common paths:**
   - `/usr/bin/whois` (Debian/Ubuntu)
   - `/usr/local/bin/whois` (manual install)
   - System PATH directories

3. **If NOT found**, script will tell you:
```
The whois not found!
Please, install the whois
    For Ubuntu/Debian:
        sudo apt update && sudo apt upgrade
        sudo apt install whois
```

4. **Install if needed:**
```bash
# Ubuntu/Debian
sudo apt install whois

# CentOS/RHEL/Fedora
sudo dnf install jwhois

# Then run script again - auto-detects!
```

---

## 📊 Comparison: With vs Without -ee

### Test 1: Without -ee (Internal only)
```bash
python3 ddec.py -d aikyam.school -c
```
**Result:** May fail or show error

### Test 2: With -ee (Internal + External fallback)
```bash
python3 ddec.py -d aikyam.school -c -ee
```
**Result:** Works reliably (fallback to external whois if needed)

---

## 🎓 Technical Details (Optional Reading)

### Script Code (ddec.py lines 254-260):
```python
# Command for external whois
if sys.platform == 'win32':
    WHOIS_COMMAND: str = f'{pathname}{SEP}winbin{SEP}whois-cygwin64{SEP}whois.exe'
else:
    WHOIS_COMMAND: str = 'whois'  # Auto-detected from PATH
```

### Auto-detection Code (ddec.py lines 460-528):
```python
def whois_check() -> None:
    """External whois availability check"""
    # Searches PATH for whois
    # Sets WHOIS_COMMAND to found location
    # If not found, prints installation instructions
```

### When -ee is used:
The script calls this function (ddec.py lines 531-593):
```python
def make_whois_query(domain: str, domain_group: str) -> Tuple:
    """Execute external whois and parse the data"""
    # Runs: subprocess.Popen([WHOIS_COMMAND, domain])
    # Parses output automatically
```

---

## ✅ Summary

### Your System Status:
```
✅ Whois installed: /usr/bin/whois
✅ Script detected it automatically
✅ -ee flag ready to use
✅ Zero configuration required
```

### Your Command (Copy-Paste Ready):
```bash
python3 ddec.py -f aikyam.txt -g -ee -i 5
```

### That's It!
Just add `-ee` to any command and it works automatically! 🎉

---

## 🔧 Troubleshooting (If Issues on VPS)

### If script says "whois not found" on VPS:

**Step 1: Check if installed**
```bash
which whois
```

**Step 2: If not found, install**
```bash
# Ubuntu/Debian VPS
sudo apt update
sudo apt install whois

# CentOS/RHEL VPS
sudo dnf install jwhois
```

**Step 3: Verify installation**
```bash
which whois
# Should show: /usr/bin/whois

whois google.com | head
# Should show WHOIS data
```

**Step 4: Run script again**
```bash
python3 ddec.py -f aikyam.txt -g -ee -i 5
# Now works automatically!
```

---

## 🎯 Final Answer to Your Question

### "Do I have to configure any whois?"

**Answer: NO! Absolutely nothing to configure!**

The `-ee` flag:
- ✅ Works automatically
- ✅ Auto-detects whois location
- ✅ Falls back gracefully
- ✅ Requires zero setup
- ✅ Just add `-ee` to your command

**Your whois is already installed at `/usr/bin/whois` and ready to go!**

---

## 🚀 Quick Start

Just run this command right now:

```bash
python3 ddec.py -f aikyam.txt -g -ee -i 5
```

It will work immediately with no additional setup! 🎉

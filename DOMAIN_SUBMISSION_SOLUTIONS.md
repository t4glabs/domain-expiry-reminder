# Domain Submission Solutions for Non-Technical Users

## Overview
Secure ways to allow users to add domains to `aikyam.txt` without VPS access.

---

## ⭐ OPTION 1: Google Forms + Apps Script (RECOMMENDED)

### Why This is Best:
- ✅ No VPS exposure at all
- ✅ Free to use
- ✅ Super easy for non-technical users
- ✅ Automatic validation
- ✅ You control approval workflow
- ✅ Works from any device

### How It Works:
1. User fills Google Form with domain name and expiry days
2. Form saves to Google Sheet
3. Apps Script validates the domain format
4. You review submissions in the sheet
5. Approved domains get formatted and added to a text output
6. You manually/automatically sync to VPS (via GitHub, email, or scheduled script)

### Setup Steps:

#### Step 1: Create Google Form
1. Go to https://forms.google.com
2. Create new form with fields:
   - **Domain Name** (Short answer, Required)
   - **Expiry Alert Days** (Short answer, Required, Default: 30)
   - **Your Email** (Email, Required)
   - **Cost per Domain** (Short answer, Optional)

#### Step 2: Link to Google Sheet
1. In Form → Responses → Create Spreadsheet
2. Form responses auto-populate Sheet

#### Step 3: Add Apps Script for Validation & Formatting

```javascript
// Open Extensions → Apps Script in Google Sheets

function onFormSubmit(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Form Responses 1");
  var lastRow = sheet.getLastRow();

  // Get submitted data
  var timestamp = sheet.getRange(lastRow, 1).getValue();
  var domain = sheet.getRange(lastRow, 2).getValue().trim().toLowerCase();
  var days = sheet.getRange(lastRow, 3).getValue();
  var email = sheet.getRange(lastRow, 4).getValue();
  var cost = sheet.getRange(lastRow, 5).getValue() || "0.00";

  // Validate domain format
  var domainRegex = /^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$/;
  var isValid = domainRegex.test(domain);

  // Validate days is a number
  var daysNum = parseInt(days);
  if (isNaN(daysNum) || daysNum < 1 || daysNum > 365) {
    isValid = false;
  }

  // Write validation status
  sheet.getRange(lastRow, 6).setValue(isValid ? "✅ Valid" : "❌ Invalid");

  // Generate formatted output
  if (isValid) {
    var formatted = domain + " " + daysNum + " cost:" + parseFloat(cost).toFixed(2);
    sheet.getRange(lastRow, 7).setValue(formatted);

    // Optional: Send confirmation email
    MailApp.sendEmail({
      to: email,
      subject: "Domain Submission Received - " + domain,
      body: "Your domain '" + domain + "' has been received and will be monitored.\n\n" +
            "Alert will be sent " + daysNum + " days before expiry."
    });
  } else {
    MailApp.sendEmail({
      to: email,
      subject: "Domain Submission Error - " + domain,
      body: "There was an error with your domain submission.\n\n" +
            "Please check the domain name format and expiry days (1-365)."
    });
  }
}

// Set up trigger: Edit → Current project's triggers → Add Trigger
// Choose: onFormSubmit, From spreadsheet, On form submit
```

#### Step 4: Create Export Sheet
Add a new sheet called "Approved Domains" with this formula in cell A1:

```
=FILTER('Form Responses 1'!G:G, 'Form Responses 1'!F:F="✅ Valid")
```

This auto-generates the formatted list ready to copy to `aikyam.txt`

#### Step 5: Sync to VPS (Choose One)

**Method A: Manual Copy (Simplest)**
- Review approved domains in sheet
- Copy formatted text
- SSH to VPS and paste into `aikyam.txt`

**Method B: GitHub Sync (Semi-automated)**
- Export sheet as CSV weekly
- Commit to private GitHub repo
- VPS pulls from GitHub via cron job

**Method C: Apps Script → VPS API (Fully automated)**
```javascript
// Call your VPS API endpoint to add domain
function syncToVPS() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Approved Domains");
  var data = sheet.getDataRange().getValues();

  var payload = {
    "domains": data.flat().filter(d => d !== "")
  };

  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "headers": {
      "Authorization": "Bearer YOUR_SECRET_TOKEN"
    }
  };

  UrlFetchApp.fetch("https://your-vps.com/api/update-domains", options);
}
```

---

## OPTION 2: Simple Web Form with API (Medium Security)

### Setup:
1. Create simple HTML form (host on GitHub Pages - free)
2. Form submits to your VPS API endpoint
3. API validates and appends to file

### Security Measures:
```python
# Flask API endpoint on VPS (example)
from flask import Flask, request, jsonify
import re
import os
from functools import wraps

app = Flask(__name__)

# Secret token authentication
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if token != os.getenv('API_SECRET_TOKEN'):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# Rate limiting (install: pip install flask-limiter)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per hour"]  # Max 5 submissions per hour per IP
)

@app.route('/api/add-domain', methods=['POST'])
@require_auth
@limiter.limit("5 per hour")
def add_domain():
    data = request.get_json()

    domain = data.get('domain', '').strip().lower()
    days = data.get('days', 30)
    cost = data.get('cost', 0.00)

    # Validate domain
    domain_regex = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$'
    if not re.match(domain_regex, domain):
        return jsonify({"error": "Invalid domain format"}), 400

    # Validate days
    try:
        days = int(days)
        if days < 1 or days > 365:
            raise ValueError
    except:
        return jsonify({"error": "Days must be 1-365"}), 400

    # Check if domain already exists
    with open('/path/to/aikyam.txt', 'r') as f:
        if domain in f.read():
            return jsonify({"error": "Domain already exists"}), 409

    # Append to file (with file locking)
    import fcntl
    formatted = f"{domain} {days} cost:{cost:.2f}\n"

    with open('/path/to/aikyam.txt', 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(formatted)
        fcntl.flock(f, fcntl.LOCK_UN)

    return jsonify({"success": True, "domain": domain}), 201

if __name__ == '__main__':
    # Only listen on localhost, use nginx as reverse proxy
    app.run(host='127.0.0.1', port=5000)
```

### HTML Form (host on GitHub Pages):
```html
<!DOCTYPE html>
<html>
<head>
    <title>Add Domain for Monitoring</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        input, button { width: 100%; padding: 10px; margin: 10px 0; font-size: 16px; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        .error { color: red; }
        .success { color: green; }
    </style>
</head>
<body>
    <h2>🔔 Add Domain for Monitoring</h2>
    <form id="domainForm">
        <label>Domain Name:</label>
        <input type="text" id="domain" placeholder="example.com" required>

        <label>Alert Days Before Expiry:</label>
        <input type="number" id="days" value="30" min="1" max="365" required>

        <label>Cost (optional):</label>
        <input type="number" id="cost" step="0.01" value="0" min="0">

        <label>Your Email (for confirmation):</label>
        <input type="email" id="email" required>

        <button type="submit">Add Domain</button>
    </form>

    <div id="message"></div>

    <script>
        document.getElementById('domainForm').addEventListener('submit', async (e) => {
            e.preventDefault();

            const domain = document.getElementById('domain').value.trim().toLowerCase();
            const days = document.getElementById('days').value;
            const cost = document.getElementById('cost').value;
            const email = document.getElementById('email').value;
            const messageDiv = document.getElementById('message');

            messageDiv.innerHTML = 'Submitting...';

            try {
                const response = await fetch('https://your-vps.com/api/add-domain', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Token': 'your-secret-token-here'  // Move to backend later
                    },
                    body: JSON.stringify({ domain, days, cost, email })
                });

                const result = await response.json();

                if (response.ok) {
                    messageDiv.innerHTML = '<p class="success">✅ Domain added successfully!</p>';
                    document.getElementById('domainForm').reset();
                } else {
                    messageDiv.innerHTML = `<p class="error">❌ Error: ${result.error}</p>`;
                }
            } catch (error) {
                messageDiv.innerHTML = '<p class="error">❌ Network error. Please try again.</p>';
            }
        });
    </script>
</body>
</html>
```

---

## OPTION 3: Telegram Bot (Easy for Regular Users)

If your users already use Telegram, create a bot:

### Python Bot Script:
```python
# Install: pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

AUTHORIZED_USERS = [123456789, 987654321]  # Telegram user IDs
DOMAINS_FILE = "/path/to/aikyam.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔔 Domain Monitoring Bot\n\n"
        "Commands:\n"
        "/add domain.com 30 - Add domain with 30 days alert\n"
        "/list - Show all monitored domains\n"
        "/help - Show this message"
    )

async def add_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("❌ Unauthorized")
        return

    try:
        domain = context.args[0].strip().lower()
        days = int(context.args[1]) if len(context.args) > 1 else 30
        cost = float(context.args[2]) if len(context.args) > 2 else 0.00

        # Validate domain
        domain_regex = r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$'
        if not re.match(domain_regex, domain):
            await update.message.reply_text("❌ Invalid domain format")
            return

        # Check if exists
        with open(DOMAINS_FILE, 'r') as f:
            if domain in f.read():
                await update.message.reply_text("⚠️ Domain already exists")
                return

        # Append
        formatted = f"{domain} {days} cost:{cost:.2f}\n"
        with open(DOMAINS_FILE, 'a') as f:
            f.write(formatted)

        await update.message.reply_text(f"✅ Added: {formatted.strip()}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}\n\nUsage: /add domain.com 30 12.50")

async def list_domains(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(DOMAINS_FILE, 'r') as f:
        domains = f.readlines()

    message = "📋 Monitored Domains:\n\n" + "".join(domains)
    await update.message.reply_text(message)

def main():
    app = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("add", add_domain))
    app.add_handler(CommandHandler("list", list_domains))

    app.run_polling()

if __name__ == '__main__':
    main()
```

Run on VPS:
```bash
# Install in tmux or screen session
pip install python-telegram-bot
python3 telegram_bot.py
```

---

## OPTION 4: Email-to-File (Simplest, No Form)

Users email you with format: `DOMAIN: example.com DAYS: 30`

Python script parses emails and updates file:

```python
import imaplib
import email
import re

def check_email_submissions():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your-email@gmail.com', 'app-password')
    mail.select('inbox')

    _, data = mail.search(None, 'SUBJECT "Add Domain"')

    for num in data[0].split():
        _, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        body = msg.get_payload(decode=True).decode()

        # Parse: DOMAIN: example.com DAYS: 30
        domain_match = re.search(r'DOMAIN:\s*([a-z0-9.-]+)', body, re.I)
        days_match = re.search(r'DAYS:\s*(\d+)', body, re.I)

        if domain_match and days_match:
            domain = domain_match.group(1).lower()
            days = days_match.group(1)

            with open('/path/to/aikyam.txt', 'a') as f:
                f.write(f"{domain} {days}\n")

            # Mark as processed
            mail.store(num, '+FLAGS', '\\Seen')

    mail.close()
    mail.logout()

# Run via cron every hour
```

---

## COMPARISON TABLE

| Solution | Security | Ease | Cost | Automation | Best For |
|----------|----------|------|------|------------|----------|
| Google Forms | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | Medium | Non-tech users, approval workflow |
| Web Form + API | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Free | High | Direct submission |
| Telegram Bot | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | High | Telegram users, quick adds |
| Email Parsing | ⭐⭐⭐ | ⭐⭐⭐ | Free | Medium | Very simple use case |

---

## 🏆 MY RECOMMENDATION

**Use Google Forms + Apps Script** because:

1. ✅ **Zero VPS exposure** - No ports opened, no API to hack
2. ✅ **Approval workflow** - You review before adding
3. ✅ **Validation built-in** - Bad entries auto-rejected
4. ✅ **Email notifications** - Users get confirmations
5. ✅ **Free forever** - No hosting costs
6. ✅ **Mobile-friendly** - Works on any device
7. ✅ **Easy for non-tech users** - Just fill a form

### Sync Methods (pick one):
- **Manual** (weekly): Copy from sheet → SSH → paste to aikyam.txt
- **Semi-auto** (GitHub): Sheet → CSV → GitHub → VPS pulls
- **Full auto** (API): Apps Script → Your VPS API endpoint

---

## QUICK START: Google Forms Method

1. **Now**: Create Google Form (5 min)
2. **Now**: Add Apps Script validation (5 min)
3. **Now**: Share form link with users
4. **Weekly**: Review sheet, copy approved domains
5. **Weekly**: SSH to VPS, paste to aikyam.txt

Total setup time: **10 minutes**
User experience: **Just fill a form**
Your effort: **5 minutes/week to review & sync**

---

Would you like me to help you set up any of these solutions? I can:
- Create the complete Google Form structure
- Write the Apps Script code
- Set up the API endpoint for your VPS
- Create the Telegram bot

Let me know which direction you prefer!

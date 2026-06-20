# Google Chat Webhook Support - Changes Documentation

This document details all changes made to add Google Chat webhook notification support to the DNS Domain Expiration Checker.

## Summary
Google Chat webhook support has been added as a third notification method alongside Email and Telegram. Users can now receive domain expiration reports directly in their Google Chat spaces.

---

## Changes Made

### 1. Configuration Constants (Lines 192-195)
**File**: `ddec.py`

**What Changed**: Added Google Chat webhook URL configuration constant

```python
# Google Chat webhook options
# Get help from https://developers.google.com/workspace/chat/quickstart/webhooks
# Webhook URL for Google Chat Space
GOOGLE_CHAT_WEBHOOK: str = os.getenv('GOOGLE_CHAT_WEBHOOK', '<INSERT YOUR WEBHOOK URL>')
```

**Why**: This allows users to configure their Google Chat webhook URL either by:
- Setting it directly in the code
- Using the `GOOGLE_CHAT_WEBHOOK` environment variable
- Providing it via command-line argument

---

### 2. CLI Arguments (Lines 1753-1765)
**File**: `ddec.py`

**What Changed**: Added two new command-line arguments

```python
parent_group.add_argument(
    '-g',
    '--use-google-chat',
    action='store_true',
    default=False,
    help='Send a warning message through Google Chat webhook (default is False)'
)
parent_group.add_argument(
    '-w',
    '--google-chat-webhook',
    help='Google Chat webhook URL (default is None)',
    metavar='URL'
)
```

**Why**:
- `-g` or `--use-google-chat`: Enables Google Chat notifications
- `-w` or `--google-chat-webhook`: Allows specifying webhook URL from command line

---

### 3. Send Function (Lines 1083-1109)
**File**: `ddec.py`

**What Changed**: Added new function to send messages to Google Chat

```python
def send_google_chat(message: str, webhook_url: str) -> None:
    """
    Sending a message through Google Chat webhook.
    :param message: str
    :param webhook_url: str
    :return: None
    """
    # Google Chat expects JSON with 'text' field
    payload: Dict = {'text': message}
    headers: Dict = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    try:
        r: Optional[Any] = requests.post(
            webhook_url,
            timeout=10,
            json=payload,
            headers=headers,
            verify=True,
        )

        if r is not None and r.status_code != 200:
            print(f'{FLR}Google Chat webhook error: {r.text}')

    except requests.exceptions.RequestException as e:
        print(f'{FRC}Google Chat error: {str(e)}')
```

**Why**:
- Google Chat webhooks require JSON POST with `text` field
- Uses proper Content-Type header: `application/json; charset=UTF-8`
- Includes error handling for failed requests

---

### 4. Report Generation Function (Lines 1112-1295)
**File**: `ddec.py`

**What Changed**: Added comprehensive report formatting function for Google Chat

```python
def make_report_for_google_chat() -> None:
    """
    Make report for send through Google Chat webhook.
    :return: None
    """
    # ... (full implementation with all domain categories)
```

**Key Features**:
- Uses Markdown formatting (`*bold*` and ` ```code blocks``` `)
- Includes all domain categories:
  - Expiring domains
  - Soon-to-expire domains
  - Error domains
  - Rate-limited domains
  - Free domains
  - Domains with WHOIS text changes
  - Cost summary
- Automatic message truncation at 4000 characters (Google Chat limit)
- Fetches webhook URL from CLI argument or environment variable

**Why**:
- Google Chat supports Markdown-style formatting (not HTML like Telegram)
- Message size limits require truncation
- Maintains same information structure as Email/Telegram reports

---

### 5. CLI Validation Logic (Lines 3054-3077)
**File**: `ddec.py`

**What Changed**: Added validation for Google Chat arguments

```python
# Updated existing validation to include Google Chat
if (not CLI.print_to_console and (CLI.file or CLI.domain)) and (
        (not CLI.use_telegram) and (not CLI.email_to) and (not CLI.use_google_chat)):
    print(
        f'{FLR}You must use at least one of the notification methods '
        f'(email, telegram, google chat or console)\n'
        f'Use --print-to-console or --email-to or/and --use-telegram or/and --use-google-chat'
    )
    sys.exit(-1)

# New validation for Google Chat webhook URL
if CLI.use_google_chat and (not CLI.google_chat_webhook):
    # Check if webhook URL is set in environment variable
    if GOOGLE_CHAT_WEBHOOK == '<INSERT YOUR WEBHOOK URL>':
        print(
            f'{FLR}You must specify Google Chat webhook URL. '
            f'Use the --google-chat-webhook option or set GOOGLE_CHAT_WEBHOOK environment variable'
        )
        sys.exit(-1)

if CLI.google_chat_webhook and (not CLI.use_google_chat):
    print(
        f'{FLR}You must enable Google Chat notifications. '
        f'Use the --use-google-chat option'
    )
    sys.exit(-1)
```

**Why**:
- Ensures at least one notification method is specified
- Validates webhook URL is provided when Google Chat is enabled
- Prevents invalid argument combinations

---

### 6. Main Function Integration (Lines 3352-3353)
**File**: `ddec.py`

**What Changed**: Added Google Chat report call in main processing flow

```python
if CLI.use_google_chat:
    make_report_for_google_chat()
```

**Location**: After email and telegram report generation, before script exit

**Why**: Integrates Google Chat into the main notification flow alongside existing methods

---

## Usage Examples

### 1. Basic Usage with Command-Line Webhook
```bash
python3 ddec.py -f domains.txt -g -w "https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYY&token=ZZZZ"
```

### 2. Using Environment Variable
```bash
export GOOGLE_CHAT_WEBHOOK="https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=YYYY&token=ZZZZ"
python3 ddec.py -f domains.txt -g
```

### 3. Combined with Other Notifications
```bash
# Send to Email, Telegram, AND Google Chat
python3 ddec.py -f domains.txt -e user@example.com -t -g -w "https://chat.googleapis.com/v1/spaces/..."
```

### 4. With Console Output
```bash
python3 ddec.py -f domains.txt -c -g -w "https://chat.googleapis.com/v1/spaces/..."
```

---

## Message Format

### Google Chat Message Structure
```
*Domains Report  [ 15.01.2026 12:30 ]*

*Domains are expiring*
```
------------------------------------------   DL
    1. example.com                            5
    2. test.com                               -2
```

*Cost*
```
------------------------------------------
For Expires   : ¥ 24.00
------------------------------------------
Total         : ¥ 24.00
```
```

**Formatting Used**:
- `*text*` for bold (section headers)
- ` ```code blocks``` ` for monospace/preformatted content
- Plain text for regular content

---

## How to Get Google Chat Webhook URL

1. Open Google Chat in browser
2. Go to the Space where you want notifications
3. Click the Space name → **Manage webhooks**
4. Click **Add webhook**
5. Give it a name (e.g., "Domain Expiration Checker")
6. Click **Save**
7. Copy the webhook URL provided
8. Use this URL with the `-w` option or set as environment variable

---

## Technical Notes

### Google Chat API Requirements
- **HTTP Method**: POST
- **Content-Type**: `application/json; charset=UTF-8`
- **Payload Format**: `{"text": "message content"}`
- **Message Size Limit**: ~4096 characters (script uses 4000 as safe limit)
- **Formatting**: Supports basic Markdown (bold, italic, code blocks)

### Differences from Telegram
| Feature | Telegram | Google Chat |
|---------|----------|-------------|
| Message format | HTML tags | Markdown |
| Bold text | `<b>text</b>` | `*text*` |
| Code blocks | `<pre>code</pre>` | ` ```code``` ` |
| Max message size | ~4000 chars | ~4000 chars |
| Requires auth | Bot token + Chat ID | Webhook URL only |
| Proxy support | Yes | No (uses standard requests) |

---

## Testing

### Test Single Domain
```bash
python3 ddec.py -d aikyam.school -g -w "YOUR_WEBHOOK_URL"
```

### Test with Small Domain List
```bash
# Create test file
echo "! Test Group" > test-domains.txt
echo "aikyam.school 30" >> test-domains.txt
echo "pattic.school 60" >> test-domains.txt

# Run test
python3 ddec.py -f test-domains.txt -c -g -w "YOUR_WEBHOOK_URL"
```

---

## Files Modified

Only one file was modified:
- **ddec.py** (main script file)

Total lines added: ~230 lines
Total lines modified: ~10 lines

---

## Compatibility

- ✅ Works with existing Email notifications
- ✅ Works with existing Telegram notifications
- ✅ Can be used standalone or combined
- ✅ No impact on existing functionality
- ✅ Backward compatible (existing scripts work without changes)

---

## Error Handling

The implementation includes error handling for:
1. Missing webhook URL (CLI validation)
2. Invalid webhook URL (HTTP request errors)
3. Network timeouts (10-second timeout)
4. Non-200 HTTP responses
5. Message size overflow (automatic truncation)

All errors are printed to console with colored output for visibility.

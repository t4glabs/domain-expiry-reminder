#!/opt/homebrew/opt/python@3.10/libexec/bin/python3
import os
import sys
import datetime
from datetime import timezone
import warnings

# Force UTC and suppress warnings
os.environ['TZ'] = 'UTC'
warnings.filterwarnings("ignore")

# Monkey patch datetime.datetime methods (CORRECT way)
original_now = datetime.datetime.now
original_utcnow = datetime.datetime.utcnow

def naive_now(*args, **kwargs):
    dt = original_now(*args, **kwargs)
    return dt.replace(tzinfo=None) if dt.tzinfo else dt

def naive_utcnow():
    dt = original_utcnow()
    return dt.replace(tzinfo=None)

# Patch the CLASS methods
datetime.datetime.now = naive_now
datetime.datetime.utcnow = naive_utcnow

# Execute original script
sys.path.insert(0, '.')
from ddec import main
sys.exit(main())

# RDAP Implementation Summary for ddec_rdap.py

## Overview
Successfully created `ddec_rdap.py` with RDAP (Registration Data Access Protocol) support for .school and .fund domains.

## Problem Solved
.school and .fund domains fail with python-whois because IANA returns empty whois server references. These domains are managed by Identity Digital/Cloudflare and use RDAP instead of traditional WHOIS.

## Changes Made

### 1. Added RDAP Configuration Constants (Lines 259-264)
Located after `UNSUPPORTED_DOMAINS` and before external whois command configuration.

```python
# RDAP-based TLDs configuration
# TLDs that require RDAP instead of traditional WHOIS
RDAP_TLDS: Dict[str, str] = {
    '.school': 'https://rdap.identitydigital.services/rdap/domain/',
    '.fund': 'https://rdap.identitydigital.services/rdap/domain/',
}
```

**Purpose**: Defines which TLDs require RDAP and their corresponding RDAP service endpoints.

### 2. Created query_rdap() Function (Lines 801-858)
Located immediately after `parse_whois_data()` function and before `calculate_expiration_days()`.

```python
def query_rdap(domain: str, rdap_url: str) -> Tuple:
    """
    Query domain information via RDAP (Registration Data Access Protocol)
    :param domain: str - domain name
    :param rdap_url: str - base RDAP URL
    :return: Tuple (whois_data, expiration_date, registrar, whois_server, ret_error)
    """
```

**Key Features**:
- Queries RDAP endpoint with proper headers and timeout
- Handles HTTP 404 (domain not found) returning error code 11
- Handles other HTTP errors returning error code 1
- Parses JSON response to extract:
  - Expiration date from `events` array (eventAction='expiration')
  - Registrar from `entities` array with role='registrar' (parses vCard format)
  - Stores full JSON as whois_data for caching/logging
  - Uses RDAP endpoint as whois_server identifier
- Handles exceptions gracefully

### 3. Modified check_domain() Function (Lines 2616-2638)
Added RDAP check logic before the existing `if CLI.use_only_external_whois:` block.

```python
# Check if domain uses RDAP
rdap_url = None
for tld, url in RDAP_TLDS.items():
    if domain_name.lower().endswith(tld):
        rdap_url = url
        break

if rdap_url:
    # Use RDAP query
    (
        whois_data,
        expiration_date,
        registrar,
        whois_server,
        ret_error
    ) = query_rdap(
        domain=domain_name,
        rdap_url=rdap_url
    )
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    # Init colorama again
    init(autoreset=True)
elif CLI.use_only_external_whois:
    # ... existing code
```

**Logic Flow**:
1. First checks if domain TLD is in RDAP_TLDS dictionary
2. If RDAP is required, calls query_rdap() and skips traditional whois
3. Otherwise, proceeds with existing logic (python-whois or external whois)
4. Properly restores stdout/stderr and reinitializes colorama

## Integration Details

- **No new imports needed**: json module already imported (line 43)
- **Type hints maintained**: Uses existing Tuple, Dict type annotations
- **Error codes consistent**: Uses error code 11 for free/not-found domains, code 1 for query errors
- **Style consistent**: Follows existing code formatting and structure
- **Colorama compatibility**: Properly handles stdout/stderr redirection

## Testing Recommendations

Test with these domains:
```bash
python ddec_rdap.py -d aikyam.school
python ddec_rdap.py -d aikyam.fund
```

Expected results based on curl tests:
- **aikyam.school**: Expiration 2026-10-04, Registration 2023-10-04
- **aikyam.fund**: Expiration 2026-07-04, Registration 2023-07-04

## Future Enhancements

To add more RDAP-based TLDs, simply update the RDAP_TLDS dictionary:
```python
RDAP_TLDS: Dict[str, str] = {
    '.school': 'https://rdap.identitydigital.services/rdap/domain/',
    '.fund': 'https://rdap.identitydigital.services/rdap/domain/',
    '.newTLD': 'https://rdap.example.com/rdap/domain/',  # Add new TLDs here
}
```

## Files Modified
- **Created**: `/Users/jinsoraj/Desktop/clones/dns-domain-expiration-checker/ddec_rdap.py`
- **Based on**: ddec.py version 0.2.26.1

## Line References
- RDAP_TLDS configuration: Lines 259-264
- query_rdap() function: Lines 801-858
- check_domain() RDAP logic: Lines 2616-2638

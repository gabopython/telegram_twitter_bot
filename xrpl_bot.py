import requests

XRPSCAN_BASE = "https://api.xrpscan.com/api/v1"

def decode_currency_code(code: str) -> str:
    """
    Decode XRPL 160-bit hex currency code to ASCII string.
    If already short text (like 'USD'), returns unchanged.
    """
    if code and len(code) <= 3 and code.isascii():
        return code

    try:
        bytes_code = bytes.fromhex(code)
        text_code = bytes_code.rstrip(b'\x00').decode('ascii', errors='ignore')
        return text_code or code
    except Exception:
        return code

def get_assets_from_issuer(issuer_address: str):
    """
    Fetch issued assets from XRPSCAN using issuer address.
    """
    url = f"{XRPSCAN_BASE}/account/{issuer_address}/assets"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    # XRPSCAN returns {"assets": [...]} usually
    if isinstance(data, dict):
        return data.get("assets") or data.get("issued") or []
    elif isinstance(data, list):
        return data
    return []

def get_token_info(token_code: str, issuer_address: str):
    """
    Fetch token info from XRPSCAN by token code + issuer.
    """
    url = f"{XRPSCAN_BASE}/token/{token_code}:{issuer_address}"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        return None
    return r.json()

def main(issuer):
    print(f"Fetching assets for issuer: {issuer}")
    assets = get_assets_from_issuer(issuer)

    if not assets:
        print("No assets found for this issuer.")
        return

    for asset in assets:
        # try to extract the currency code
        raw_code = asset.get("currency") or asset.get("code") or asset.get("token") or asset.get("name")
        if not raw_code:
            print("Skipping asset without code field:", asset)
            continue

        token_code = decode_currency_code(raw_code)
        print("\n==============================")
        print("Raw Code:", raw_code)
        print("Decoded Token Code:", token_code)

        info = get_token_info(token_code, issuer)
        if not info:
            print("Could not fetch token info from XRPSCAN for", token_code)
            continue

        # Display fields XRPSCAN returns (adapt these to your needs)
        print("Ticker / Code:", info.get("code") or token_code)
        print("Name:", info.get("name"))
        print("Supply:", info.get("supply"))
        print("Market Cap:", info.get("marketcap"))
        print("Price (USD):", info.get("price"))
        print("AMMs (Liquidity Pools):", info.get("amms"))

if __name__ == "__main__":
    # Replace with your issuer address
    issuer_address = "rfmS3zqrQrka8wVyhXifEeyTwe8AMz2Yhw"
    main(issuer_address)


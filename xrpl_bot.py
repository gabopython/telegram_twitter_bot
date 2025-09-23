from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountObjects

def get_tickers_by_issuer(issuer_address):
    client = JsonRpcClient("https://s2.ripple.com:51234/")  # Mainnet
    response = client.request(AccountObjects(account=issuer_address))
    tickers = set()

    for obj in response.result.get("account_objects", []):
        if obj.get("LedgerEntryType") == "RippleState":
            # Tokens issued by this account
            high_limit = obj.get("HighLimit")
            low_limit = obj.get("LowLimit")

            # Identify which side belongs to issuer
            if high_limit and high_limit.get("issuer") == issuer_address:
                tickers.add(high_limit.get("currency"))
            if low_limit and low_limit.get("issuer") == issuer_address:
                tickers.add(low_limit.get("currency"))

    return list(tickers)

# Example usage
issuer_address = "rfmS3zqrQrka8wVyhXifEeyTwe8AMz2Yhw"
tickers = get_tickers_by_issuer(issuer_address)
print("Tickers issued by this address:", tickers)

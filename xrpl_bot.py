from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountCurrencies, AccountLines

# XRPL Testnet RPC URL (use mainnet if needed)
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(JSON_RPC_URL)

def get_token_info(issuer_address: str):
    # Get all currencies this issuer issues
    currencies_request = AccountCurrencies(
        account=issuer_address,
        ledger_index="validated"
    )
    currencies_response = client.request(currencies_request).result

    # Get trustlines for details
    lines_request = AccountLines(
        account=issuer_address,
        ledger_index="validated"
    )
    lines_response = client.request(lines_request).result

    return {
        "issuer": issuer_address,
        "issued_currencies": currencies_response.get("receive_currencies", []),
        "trustlines": lines_response.get("lines", [])
    }

if __name__ == "__main__":
    issuer = 'rfmS3zqrQrka8wVyhXifEeyTwe8AMz2Yhw'
    info = get_token_info(issuer)

    print("\n=== Token Info ===")
    print(f"Issuer: {info['issuer']}")
    print("Issued Currencies:", info["issued_currencies"])
    print("\nTrustlines:")
    for line in info["trustlines"]:
        print(f"- Currency: {line['currency']}, Balance: {line['balance']}, Limit: {line['limit']}")

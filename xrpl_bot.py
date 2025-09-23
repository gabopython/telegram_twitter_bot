from xrpl.clients import JsonRpcClient

# XRPL Mainnet endpoint
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)



from xrpl.models.requests import AccountTx

address = "YOUR_XRPL_ADDRESS"  # Replace with your real XRPL wallet address

account_tx = AccountTx(
    account=address,
    ledger_index_min=-1,
    ledger_index_max=-1,
    limit=10  # how many tx to fetch
)

response = client.request(account_tx)
transactions = response.result["transactions"]

for tx in transactions:
    # tx["tx"] is the actual transaction data
    tx_data = tx["tx"]
    print("Type:", tx_data["TransactionType"])
    print("Hash:", tx_data["hash"])
    print("Amount:", tx_data.get("Amount"))
    print("Date:", tx_data["date"])
    print("-" * 40)

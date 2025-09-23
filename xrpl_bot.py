
import xrpl

# Connect to the XRPL Testnet
from xrpl.clients import JsonRpcClient

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"  # Testnet URL
client = JsonRpcClient(JSON_RPC_URL)

from xrpl.wallet import generate_faucet_wallet

# Generate and fund a wallet on Testnet
test_wallet = generate_faucet_wallet(client, debug=True)
print("Address:", test_wallet.classic_address)
print("Seed:", test_wallet.seed)
from xrpl.models.requests import AccountInfo

acct_info = AccountInfo(
    account=test_wallet.classic_address,
    ledger_index="validated",
    strict=True
)
response = client.request(acct_info)
print(response.result)
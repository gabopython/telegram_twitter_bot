import requests
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.utils import xrp_to_drops

# --- CONFIG ---
TESTNET_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(TESTNET_URL)
    # Sender's classic address
SEED = "sEd7uQvDu6nAPEnXBfFc9yooZEZm7e8"    # Receiver's seed
# ----------------

def get_receiver_address(seed: str) -> str:
    """Derive classic address from seed using xrpl 4.x Wallet API."""
    wallet = Wallet.from_seed(seed)
    return wallet.classic_address

def get_account_transactions(address: str, limit: int = 500):
    """Fetch recent transactions for the account using JSON-RPC request."""
    payload = {
        "method": "account_tx",
        "params": [
            {
                "account": address,
                "ledger_index_min": -1,
                "ledger_index_max": -1,
                "limit": limit,
                "binary": False,
                "forward": False,
            }
        ]
    }
    response = requests.post(TESTNET_URL, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

def find_payments_from_sender(tx_data: dict, sender: str, receiver: str):
    """Return a list of Payment txs where sender -> receiver."""
    matches = []
    txs = tx_data.get("result", {}).get("transactions", [])
    for t in txs:
        tx = t.get("tx", {})
        meta = t.get("meta", {})
        if tx.get("TransactionType") != "Payment":
            continue
        if tx.get("Account") == sender and tx.get("Destination") == receiver:
            matches.append({
                "hash": tx.get("hash"),
                "amount": tx.get("Amount"),
                "result": meta.get("TransactionResult"),
                "validated": t.get("validated", False)
            })
    return matches

def get_payment_info(sender_address) -> dict:
    receiver_address = get_receiver_address(SEED)

    txs = get_account_transactions(receiver_address, limit=1000)
    results = find_payments_from_sender(txs, sender_address , receiver_address)

    if not results:
        return None

    last_tx = results[0]
    drops = last_tx["amount"]
    # Convert drops (string of digits or int) to XRP float when possible
    if isinstance(drops, (int, float)) or (isinstance(drops, str) and drops.isdigit()):
        amount = int(drops) / 1_000_000
    else:
        amount = drops  # keep as-is for issued currencies or unexpected formats

    payment = {
        "amount": amount,
        "hash": last_tx["hash"],
    }

    return payment

def send_xrp(destination: str, amount: float):
    """Send XRP to a given address using xrpl-py 4.x on the Testnet."""
    wallet = Wallet.from_seed(SEED)

    # Create the payment transaction
    payment = Payment(
        account=wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=destination,
    )

    # Autofill missing fields like fee and sequence
    payment = autofill(payment, client)

    # Sign the transaction
    signed_tx = sign(payment, wallet)

    # Submit and wait for validation
    result = submit_and_wait(signed_tx, client)

    # Return simplified result
    return result.result.get("hash")

if __name__ == "__main__":
    send_xrp(   "rDo9REgtLV4cAXg1r3XJytxUAWvrAgrTmY", 5)

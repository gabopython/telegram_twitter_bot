from xrpl.clients import JsonRpcClient

client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

import requests
from xrpl.clients import JsonRpcClient
from xrpl.models import AccountObjects
from xrpl.models.requests import AccountObjects

def get_token_info(issuer_address):
    # Initialize the client
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

    # Fetch account objects
    account_objects = client.request(AccountObjects(account=issuer_address))

    # Extract token information
    tokens = []
    for obj in account_objects.result['account_objects']:
        if obj['LedgerEntryType'] == 'RippleState':
            currency = obj['Currency']
            if currency != 'XRP':
                token_info = {
                    'currency': currency,
                    'issuer': obj['Account'],
                    'balance': obj['Balance']
                }
                tokens.append(token_info)

    return tokens

# Example usage
issuer_address = ''
tokens = get_token_info(issuer_address)
for token in tokens:
    print(f"Currency: {token['currency']}, Issuer: {token['issuer']}, Balance: {token['balance']}")

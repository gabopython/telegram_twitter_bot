import requests
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import GatewayBalances

JSON_RPC_URL = "https://s1.ripple.com:51234"
client = JsonRpcClient(JSON_RPC_URL)

def get_issued_token(issuer_address):
    req = GatewayBalances(account=issuer_address, ledger_index="validated")
    res = client.request(req).result
    issued = res.get("obligations", {})
    if not issued:
        return None
    symbol = list(issued.keys())[0]
    return symbol

def search_on_dexscreener(symbol):
    url = f"https://api.dexscreener.com/latest/dex/search/?q={symbol}"
    res = requests.get(url).json()
    return res

def get_token_info(issuer):

    dexs_data = search_on_dexscreener(issuer)
    try:
        token = f"Market Cap: {dexs_data['pairs'][0]['marketCap']} USD\n\n"
    except Exception as e:
        token = f"Failed to get market cap: {e}\n"

    symbol = get_issued_token(issuer)
    if len(symbol) == 40:
        symbol_text = bytes.fromhex(symbol).decode("utf-8")
    else:    
        symbol_text = symbol   
    token += f"Ticker: {symbol_text}\n\n"

    url = 'https://firstledger.net/token/' + issuer + '/' + symbol
    token += url + '\n\n'+"Is this the token you’d like to promote?\nReply with Y for Yes or N for No"
    
    return token, symbol_text, url


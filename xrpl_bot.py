import requests
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import GatewayBalances, BookOffers

# XRPL Mainnet client
JSON_RPC_URL = "https://s1.ripple.com:51234"
client = JsonRpcClient(JSON_RPC_URL)

# Issuer address
issuer_address = "rhCAT4hRdi2Y9puNdkpMzxrdKa5wkppR62"

# 1. Get tokens issued by issuer
gateway_request = GatewayBalances(
    account=issuer_address,
    ledger_index="validated",
)
gateway_response = client.request(gateway_request)
obligations = gateway_response.result.get("obligations", {})

print(f"Issuer: {issuer_address}")
print("Tokens issued (raw obligations):")
print(obligations)

# 2. Get price in XRP from DEX
def get_token_xrp_price(currency, issuer):
    """
    Gets the best ask price for currency/XRP from orderbook.
    """
    book_request = BookOffers(
        taker_gets={"currency": "XRP"},
        taker_pays={"currency": currency, "issuer": issuer},
        ledger_index="validated",
    )
    response = client.request(book_request)
    offers = response.result.get("offers", [])
    if not offers:
        return None
    
    best = offers[0]
    gets = int(best["TakerGets"]) / 1_000_000   # drops → XRP
    pays = float(best["TakerPays"]["value"])    # Token units
    price = gets / pays if pays != 0 else None
    return price

# 3. Get XRP/USD price (from CoinGecko)
def get_xrp_usd_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "ripple", "vs_currencies": "usd"}
    response = requests.get(url, params=params)
    data = response.json()
    return data["ripple"]["usd"]

xrp_usd_price = get_xrp_usd_price()
print(f"\nCurrent XRP/USD price: ${xrp_usd_price:.4f}")

# 4. Show ticker + market cap in USD
print("\nToken Market Caps in USD:")
for ticker, supply in obligations.items():
    price_xrp = get_token_xrp_price(ticker, issuer_address)
    if price_xrp:
        market_cap_xrp = float(supply) * price_xrp
        market_cap_usd = market_cap_xrp * xrp_usd_price
        print(f"Ticker: {ticker} | Supply: {supply} | Price: {price_xrp:.6f} XRP | Market Cap: ${market_cap_usd:,.2f}")
    else:
        print(f"Ticker: {ticker} | Supply: {supply} | No XRP market found")

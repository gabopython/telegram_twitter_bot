import requests
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import GatewayBalances, BookOffers

JSON_RPC_URL = "https://s1.ripple.com:51234"
client = JsonRpcClient(JSON_RPC_URL)

def get_token_info(issuer_address):
    # 1. Get tokens issued by issuer
    gateway_request = GatewayBalances(
        account=issuer_address,
        ledger_index="validated",
    )
    try:
        gateway_response = client.request(gateway_request)
    except Exception:
        return "incorrect address"
    if "error" in gateway_response.result:
        return "incorrect address"
    obligations = gateway_response.result.get("obligations", {})
    token = f"Issuer: {issuer_address}\nTokens issued (raw obligations):\n{obligations}"

    # 2. Get XRP/USD price (from CoinGecko)
    def get_xrp_usd_price():
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "ripple", "vs_currencies": "usd"}
        response = requests.get(url, params=params)
        data = response.json()
        return data["ripple"]["usd"]

    # 3. Get price in XRP from DEX
    def get_token_xrp_price(currency, issuer):
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
        # TakerGets can be either a string (drops) or a dict (for tokens)
        if isinstance(best["TakerGets"], str):
            gets = int(best["TakerGets"]) / 1_000_000   # drops → XRP
        elif isinstance(best["TakerGets"], dict) and best["TakerGets"].get("currency") == "XRP":
            gets = float(best["TakerGets"]["value"])
        else:
            return None
        # TakerPays can be either a string or a dict
        if isinstance(best["TakerPays"], dict):
            pays = float(best["TakerPays"]["value"])
        elif isinstance(best["TakerPays"], str):
            pays = int(best["TakerPays"]) / 1_000_000
        else:
            return None
        price = gets / pays if pays != 0 else None
        return price

    xrp_usd_price = get_xrp_usd_price()
    token += f"\nCurrent XRP/USD price: ${xrp_usd_price:.4f}\n"

    token += "\nToken Market Caps in USD:\n"
    for ticker, supply in obligations.items():
        price_xrp = get_token_xrp_price(ticker, issuer_address)
        if price_xrp:
            market_cap_xrp = float(supply) * price_xrp
            market_cap_usd = market_cap_xrp * xrp_usd_price
            token += (
                f"Ticker: {ticker} | Supply: {supply} | Price: {price_xrp:.6f} XRP | "
                f"Market Cap: ${market_cap_usd:,.2f}\n"
            )
        else:
            token += f"Ticker: {ticker} | Supply: {supply} | No XRP market found\n"
    return token